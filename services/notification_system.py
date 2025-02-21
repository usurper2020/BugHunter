"""
Notification system for the BugHunter application.
Handles alerts, notifications, and user communication.
"""

import logging
import json
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from dataclasses import dataclass
import aiohttp

@dataclass
class Notification:
    """Represents a notification"""
    id: str
    type: str
    title: str
    message: str
    severity: str
    recipient_ids: List[int]
    metadata: Dict[str, Any]
    created_at: str
    delivered: bool = False

class NotificationSystem:
    """Manages notifications and alerts"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.NotificationSystem')
        self.config: Dict[str, Any] = {}
        self.notifications: Dict[str, Notification] = {}
        self.email_config: Dict[str, str] = {}
        self.slack_config: Dict[str, str] = {}
        self.webhook_urls: Dict[str, str] = {}
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize notification system"""
        try:
            # Load configuration
            config_file = Path('config/notification_config.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            
            # Set up email configuration
            self.email_config = self.config.get('email', {})
            if not self.email_config:
                self.logger.warning("Email notifications not configured")
            
            # Set up Slack configuration
            self.slack_config = self.config.get('slack', {})
            if not self.slack_config:
                self.logger.warning("Slack notifications not configured")
            
            # Set up webhook URLs
            self.webhook_urls = self.config.get('webhooks', {})
            
            self.initialized = True
            self.logger.info("Notification system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Notification system initialization failed: {str(e)}")
            return False
    
    async def send_notification(self, notification: Notification) -> bool:
        """Send a notification through configured channels"""
        try:
            # Store notification
            self.notifications[notification.id] = notification
            
            # Determine notification channels based on severity
            channels = self._get_channels_for_severity(notification.severity)
            
            # Send through each channel
            tasks = []
            for channel in channels:
                if channel == 'email':
                    tasks.append(self._send_email_notification(notification))
                elif channel == 'slack':
                    tasks.append(self._send_slack_notification(notification))
                elif channel == 'webhook':
                    tasks.append(self._send_webhook_notification(notification))
            
            # Wait for all notifications to be sent
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check if any channel succeeded
            success = any(result is True for result in results if not isinstance(result, Exception))
            
            if success:
                notification.delivered = True
                self.logger.info(f"Notification {notification.id} delivered successfully")
            else:
                self.logger.error(f"Failed to deliver notification {notification.id} through any channel")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send notification: {str(e)}")
            return False
    
    def _get_channels_for_severity(self, severity: str) -> List[str]:
        """Determine notification channels based on severity"""
        severity_channels = {
            'critical': ['email', 'slack', 'webhook'],
            'high': ['email', 'slack'],
            'medium': ['slack'],
            'low': ['slack']
        }
        return severity_channels.get(severity.lower(), ['slack'])
    
    async def _send_email_notification(self, notification: Notification) -> bool:
        """Send notification via email"""
        try:
            if not self.email_config:
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender']
            msg['Subject'] = f"BugHunter Alert: {notification.title}"
            
            # Add HTML content
            html_content = self._generate_email_html(notification)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send to each recipient
            for recipient_id in notification.recipient_ids:
                recipient_email = self._get_user_email(recipient_id)
                if not recipient_email:
                    continue
                
                msg['To'] = recipient_email
                
                # Connect to SMTP server
                with smtplib.SMTP_SSL(
                    self.email_config['smtp_server'],
                    self.email_config['smtp_port']
                ) as server:
                    server.login(
                        self.email_config['username'],
                        self.email_config['password']
                    )
                    server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {str(e)}")
            return False
    
    async def _send_slack_notification(self, notification: Notification) -> bool:
        """Send notification via Slack"""
        try:
            if not self.slack_config:
                return False
            
            webhook_url = self.slack_config['webhook_url']
            
            # Prepare message payload
            payload = {
                "text": f"*{notification.title}*",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": notification.title
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": notification.message
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:* {notification.severity}"
                            }
                        ]
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    return response.status == 200
            
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {str(e)}")
            return False
    
    async def _send_webhook_notification(self, notification: Notification) -> bool:
        """Send notification via webhook"""
        try:
            # Send to all configured webhooks
            for webhook_name, webhook_url in self.webhook_urls.items():
                try:
                    payload = {
                        "id": notification.id,
                        "type": notification.type,
                        "title": notification.title,
                        "message": notification.message,
                        "severity": notification.severity,
                        "metadata": notification.metadata,
                        "timestamp": notification.created_at
                    }
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post(webhook_url, json=payload) as response:
                            if response.status != 200:
                                self.logger.warning(f"Webhook {webhook_name} returned status {response.status}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to send to webhook {webhook_name}: {str(e)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook notifications: {str(e)}")
            return False
    
    def _generate_email_html(self, notification: Notification) -> str:
        """Generate HTML content for email notification"""
        return f"""
        <html>
            <body>
                <h2>{notification.title}</h2>
                <p>{notification.message}</p>
                <p><strong>Severity:</strong> {notification.severity}</p>
                <hr>
                <p><small>Generated by BugHunter at {notification.created_at}</small></p>
            </body>
        </html>
        """
    
    def _get_user_email(self, user_id: int) -> Optional[str]:
        """Get user's email address"""
        try:
            # TODO: Implement user email lookup
            return None
        except Exception as e:
            self.logger.error(f"Failed to get user email: {str(e)}")
            return None
    
    def get_notification_history(self, user_id: int) -> List[Notification]:
        """Get notification history for a user"""
        try:
            return [
                notif for notif in self.notifications.values()
                if user_id in notif.recipient_ids
            ]
        except Exception as e:
            self.logger.error(f"Failed to get notification history: {str(e)}")
            return []
    
    def mark_as_read(self, notification_id: str, user_id: int) -> bool:
        """Mark a notification as read for a user"""
        try:
            if notification_id not in self.notifications:
                return False
            
            notification = self.notifications[notification_id]
            if user_id not in notification.recipient_ids:
                return False
            
            # TODO: Implement notification read status tracking
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to mark notification as read: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup notification system resources"""
        try:
            self.notifications.clear()
            self.initialized = False
            self.logger.info("Notification system resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Notification system cleanup failed: {str(e)}")
