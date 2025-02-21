"""
User authentication service for the BugHunter application.
Handles user authentication, authorization, and session management.
"""

import logging
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
import bcrypt
from sqlalchemy.orm import Session

class UserAuth:
    """Manages user authentication and authorization"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.UserAuth')
        self.current_user = None
        self.session_token = None
        self.secret_key = self._load_or_generate_secret()
    
    def _load_or_generate_secret(self) -> bytes:
        """Load or generate secret key for JWT"""
        try:
            secret_file = Path('config/jwt_secret.key')
            if secret_file.exists():
                return secret_file.read_bytes()
            else:
                # Generate new secret
                import os
                secret = os.urandom(32)
                secret_file.parent.mkdir(exist_ok=True)
                secret_file.write_bytes(secret)
                return secret
        except Exception as e:
            self.logger.error(f"Error handling secret key: {str(e)}")
            raise
    
    def verify_credentials(self, username: str, password: str) -> Dict[str, Any]:
        """Verify user credentials and return authentication result"""
        try:
            from models import User
            from services.database import DatabaseManager
            
            db = DatabaseManager()
            with db.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                
                if not user:
                    return {'status': 'error', 'message': 'User not found'}
                
                if not bcrypt.checkpw(password.encode(), user.password_hash):
                    return {'status': 'error', 'message': 'Invalid password'}
                
                # Generate session token
                token = self._generate_token(user.id)
                
                self.current_user = user
                self.session_token = token
                
                return {
                    'status': 'success',
                    'user': user,
                    'token': token,
                    'role': user.role
                }
                
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_token(self, user_id: int) -> str:
        """Generate JWT token for user session"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow()
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        except Exception as e:
            self.logger.error(f"Token generation error: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.error(f"Invalid token: {str(e)}")
            return None
    
    def check_permission(self, required_role: str) -> bool:
        """Check if current user has required role"""
        try:
            if not self.current_user:
                return False
            
            # Admin has all permissions
            if self.current_user.role == 'admin':
                return True
            
            return self.current_user.role == required_role
            
        except Exception as e:
            self.logger.error(f"Permission check error: {str(e)}")
            return False
    
    def logout(self) -> bool:
        """Log out current user"""
        try:
            self.current_user = None
            self.session_token = None
            return True
        except Exception as e:
            self.logger.error(f"Logout error: {str(e)}")
            return False
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            from models import User
            from services.database import DatabaseManager
            
            db = DatabaseManager()
            with db.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                
                if not user:
                    return False
                
                if not bcrypt.checkpw(old_password.encode(), user.password_hash):
                    return False
                
                # Hash new password
                password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                user.password_hash = password_hash
                
                session.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Password change error: {str(e)}")
            return False
