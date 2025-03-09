import os
import json
from datetime import datetime
from typing import Dict, List

class Notification:
    """Handles notifications for users"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'notifications')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def send_notification(self, user_id: str, message: str) -> Dict:
        """Send a notification to a user"""
        try:
            notification = {
                "user_id": user_id,
                "message": message,
                "timestamp": str(datetime.now())
            }
            
            # Save notification
            filename = os.path.join(self.data_dir, f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(filename, 'w') as f:
                json.dump(notification, f, indent=2)
                
            return {
                "status": "success",
                "message": "Notification sent successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_notifications(self, user_id: str) -> Dict:
        """Get all notifications for a user"""
        try:
            notifications = []
            for filename in os.listdir(self.data_dir):
                if not filename.endswith('.json'):
                    continue
                    
                with open(os.path.join(self.data_dir, filename)) as f:
                    notification = json.load(f)
                    if notification["user_id"] == user_id:
                        notifications.append(notification)
                        
            return {
                "status": "success",
                "notifications": notifications
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def clear_notifications(self, user_id: str) -> Dict:
        """Clear all notifications for a user"""
        try:
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(self.data_dir, filename)) as f:
                        notification = json.load(f)
                        if notification["user_id"] == user_id:
                            os.remove(os.path.join(self.data_dir, filename))
                            
            return {
                "status": "success",
                "message": "Notifications cleared successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
