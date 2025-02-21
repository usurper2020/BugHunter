"""
Collaboration system for the BugHunter application.
Handles team collaboration, sharing, and real-time updates.
"""

import logging
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from dataclasses import dataclass
from websockets.server import WebSocketServerProtocol
import websockets

@dataclass
class CollaborationSession:
    """Represents an active collaboration session"""
    session_id: str
    owner_id: int
    participants: Set[int]
    scan_id: Optional[str]
    created_at: datetime
    status: str

@dataclass
class CollaborationMessage:
    """Represents a collaboration message"""
    type: str
    sender_id: int
    content: Dict[str, Any]
    timestamp: str

class CollaborationSystem:
    """Manages team collaboration and real-time communication"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.CollaborationSystem')
        self.sessions: Dict[str, CollaborationSession] = {}
        self.connections: Dict[int, WebSocketServerProtocol] = {}
        self.server = None
        self.initialized = False
    
    async def initialize(self) -> bool:
        """Initialize collaboration system"""
        try:
            # Load configuration
            config_file = Path('config/collaboration_config.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            
            # Start WebSocket server
            host = self.config.get('host', 'localhost')
            port = self.config.get('port', 8765)
            
            self.server = await websockets.serve(
                self._handle_connection,
                host,
                port
            )
            
            self.initialized = True
            self.logger.info(f"Collaboration system initialized on {host}:{port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Collaboration system initialization failed: {str(e)}")
            return False
    
    async def create_session(self, owner_id: int, scan_id: Optional[str] = None) -> str:
        """Create a new collaboration session"""
        try:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{owner_id}"
            
            session = CollaborationSession(
                session_id=session_id,
                owner_id=owner_id,
                participants={owner_id},
                scan_id=scan_id,
                created_at=datetime.now(),
                status='active'
            )
            
            self.sessions[session_id] = session
            
            # Notify owner
            await self._notify_user(
                owner_id,
                CollaborationMessage(
                    type='session_created',
                    sender_id=owner_id,
                    content={'session_id': session_id},
                    timestamp=datetime.now().isoformat()
                )
            )
            
            self.logger.info(f"Created collaboration session: {session_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Session creation failed: {str(e)}")
            raise
    
    async def join_session(self, session_id: str, user_id: int) -> bool:
        """Join an existing collaboration session"""
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Session not found: {session_id}")
            
            session = self.sessions[session_id]
            
            # Add participant
            session.participants.add(user_id)
            
            # Notify all participants
            message = CollaborationMessage(
                type='user_joined',
                sender_id=user_id,
                content={'session_id': session_id, 'user_id': user_id},
                timestamp=datetime.now().isoformat()
            )
            
            await self._broadcast_to_session(session_id, message)
            
            self.logger.info(f"User {user_id} joined session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to join session: {str(e)}")
            return False
    
    async def leave_session(self, session_id: str, user_id: int) -> bool:
        """Leave a collaboration session"""
        try:
            if session_id not in self.sessions:
                return False
            
            session = self.sessions[session_id]
            
            # Remove participant
            session.participants.remove(user_id)
            
            # Notify remaining participants
            message = CollaborationMessage(
                type='user_left',
                sender_id=user_id,
                content={'session_id': session_id, 'user_id': user_id},
                timestamp=datetime.now().isoformat()
            )
            
            await self._broadcast_to_session(session_id, message)
            
            # Close session if empty
            if not session.participants:
                await self.close_session(session_id)
            
            self.logger.info(f"User {user_id} left session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to leave session: {str(e)}")
            return False
    
    async def send_message(self, session_id: str, user_id: int, content: Dict[str, Any]) -> bool:
        """Send a message to session participants"""
        try:
            if session_id not in self.sessions:
                raise ValueError(f"Session not found: {session_id}")
            
            message = CollaborationMessage(
                type='message',
                sender_id=user_id,
                content=content,
                timestamp=datetime.now().isoformat()
            )
            
            await self._broadcast_to_session(session_id, message)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            return False
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle new WebSocket connection"""
        try:
            # Authenticate connection
            auth_message = await websocket.recv()
            auth_data = json.loads(auth_message)
            
            user_id = auth_data.get('user_id')
            if not user_id:
                await websocket.close(1008, "Authentication required")
                return
            
            # Store connection
            self.connections[user_id] = websocket
            
            try:
                async for message in websocket:
                    await self._handle_message(user_id, message)
            finally:
                # Cleanup on disconnect
                if user_id in self.connections:
                    del self.connections[user_id]
                
                # Leave all active sessions
                for session_id in list(self.sessions.keys()):
                    if user_id in self.sessions[session_id].participants:
                        await self.leave_session(session_id, user_id)
                
        except Exception as e:
            self.logger.error(f"WebSocket handler error: {str(e)}")
    
    async def _handle_message(self, user_id: int, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'join_session':
                await self.join_session(data['session_id'], user_id)
            elif message_type == 'leave_session':
                await self.leave_session(data['session_id'], user_id)
            elif message_type == 'message':
                await self.send_message(data['session_id'], user_id, data['content'])
            else:
                self.logger.warning(f"Unknown message type: {message_type}")
                
        except Exception as e:
            self.logger.error(f"Message handler error: {str(e)}")
    
    async def _notify_user(self, user_id: int, message: CollaborationMessage):
        """Send notification to specific user"""
        try:
            if user_id in self.connections:
                websocket = self.connections[user_id]
                await websocket.send(json.dumps(message.__dict__))
        except Exception as e:
            self.logger.error(f"Failed to notify user {user_id}: {str(e)}")
    
    async def _broadcast_to_session(self, session_id: str, message: CollaborationMessage):
        """Broadcast message to all session participants"""
        try:
            session = self.sessions[session_id]
            for user_id in session.participants:
                await self._notify_user(user_id, message)
        except Exception as e:
            self.logger.error(f"Broadcast failed for session {session_id}: {str(e)}")
    
    async def close_session(self, session_id: str) -> bool:
        """Close a collaboration session"""
        try:
            if session_id not in self.sessions:
                return False
            
            session = self.sessions[session_id]
            
            # Notify participants
            message = CollaborationMessage(
                type='session_closed',
                sender_id=session.owner_id,
                content={'session_id': session_id},
                timestamp=datetime.now().isoformat()
            )
            
            await self._broadcast_to_session(session_id, message)
            
            # Remove session
            del self.sessions[session_id]
            
            self.logger.info(f"Closed collaboration session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to close session: {str(e)}")
            return False
    
    async def cleanup(self):
        """Cleanup collaboration system resources"""
        try:
            # Close all sessions
            for session_id in list(self.sessions.keys()):
                await self.close_session(session_id)
            
            # Close all connections
            for websocket in self.connections.values():
                await websocket.close()
            
            # Stop server
            if self.server:
                self.server.close()
                await self.server.wait_closed()
            
            self.initialized = False
            self.logger.info("Collaboration system resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Collaboration system cleanup failed: {str(e)}")
