from datetime import datetime, timedelta
import jwt
from typing import Dict, Any, Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from config import config
from logger_config import logger_config
from database import DatabaseManager
from src.models import User, UserRole
from middleware import error_handler

logger = logger_config.get_logger(__name__)
ph = PasswordHasher()

class AuthService:
    """Service for handling authentication and authorization"""

    @staticmethod
    @error_handler
    def register_user(username: str, password: str, role: str = 'user') -> Dict[str, Any]:
        """Register a new user"""
        # Validate password complexity
        if not AuthService._validate_password_complexity(password):
            return {
                'success': False,
                'message': 'Password does not meet complexity requirements'
            }

        with DatabaseManager.get_session() as session:
            # Check if username exists
            if session.query(User).filter(User.username == username).first():
                return {
                    'success': False,
                    'message': 'Username already exists'
                }

            # Hash password with Argon2
            password_hash = ph.hash(password)

            # Create new user
            user = User(
                username=username,
                password_hash=password_hash,
                role=UserRole(role)
            )
            session.add(user)

            logger_config.log_security_event(
                'user_registered',
                {'username': username, 'role': role}
            )

            return {
                'success': True,
                'message': 'User registered successfully',
                'user': user.to_dict()
            }

    @staticmethod
    @error_handler
    def login(username: str, password: str, ip_address: str) -> Dict[str, Any]:
        """Authenticate a user and return JWT token"""
        with DatabaseManager.get_session() as session:
            user = session.query(User).filter(User.username == username).first()

            if not user:
                logger_config.log_security_event(
                    'login_failed',
                    {'username': username, 'reason': 'user_not_found', 'ip': ip_address}
                )
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }

            # Check if account is locked
            if AuthService._is_account_locked(user):
                logger_config.log_security_event(
                    'login_failed',
                    {'username': username, 'reason': 'account_locked', 'ip': ip_address}
                )
                return {
                    'success': False,
                    'message': 'Account is locked. Please try again later.'
                }

            try:
                # Verify password
                ph.verify(user.password_hash, password)

                # Reset login attempts on successful login
                user.login_attempts = 0
                user.locked_until = None
                user.last_login = datetime.utcnow()

                # Generate JWT token
                token = AuthService._generate_token(user)

                logger_config.log_security_event(
                    'login_successful',
                    {'username': username, 'ip': ip_address}
                )

                return {
                    'success': True,
                    'message': 'Login successful',
                    'token': token,
                    'user': user.to_dict()
                }

            except VerifyMismatchError:
                # Increment login attempts
                user.login_attempts += 1

                # Lock account if max attempts exceeded
                if user.login_attempts >= config.get('MAX_LOGIN_ATTEMPTS'):
                    user.locked_until = datetime.utcnow() + timedelta(
                        minutes=config.get('LOGIN_LOCKOUT_MINUTES')
                    )
                    logger_config.log_security_event(
                        'account_locked',
                        {
                            'username': username,
                            'ip': ip_address,
                            'attempts': user.login_attempts
                        }
                    )

                logger_config.log_security_event(
                    'login_failed',
                    {
                        'username': username,
                        'reason': 'invalid_password',
                        'attempts': user.login_attempts,
                        'ip': ip_address
                    }
                )

                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }

    @staticmethod
    @error_handler
    def change_password(user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change a user's password"""
        if not AuthService._validate_password_complexity(new_password):
            return {
                'success': False,
                'message': 'New password does not meet complexity requirements'
            }

        with DatabaseManager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return {
                    'success': False,
                    'message': 'User not found'
                }

            try:
                # Verify old password
                ph.verify(user.password_hash, old_password)

                # Hash and set new password
                user.password_hash = ph.hash(new_password)
                user.updated_at = datetime.utcnow()

                logger_config.log_security_event(
                    'password_changed',
                    {'user_id': user_id}
                )

                return {
                    'success': True,
                    'message': 'Password changed successfully'
                }

            except VerifyMismatchError:
                logger_config.log_security_event(
                    'password_change_failed',
                    {'user_id': user_id, 'reason': 'invalid_old_password'}
                )
                return {
                    'success': False,
                    'message': 'Invalid old password'
                }

    @staticmethod
    def _validate_password_complexity(password: str) -> bool:
        """Validate password complexity requirements"""
        min_length = config.get('PASSWORD_MIN_LENGTH')
        if len(password) < min_length:
            return False

        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            return False

        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            return False

        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            return False

        # Check for at least one special character
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        if not any(c in special_chars for c in password):
            return False

        return True

    @staticmethod
    def _is_account_locked(user: User) -> bool:
        """Check if user account is locked"""
        if user.locked_until and user.locked_until > datetime.utcnow():
            return True
        return False

    @staticmethod
    def _generate_token(user: User) -> str:
        """Generate JWT token for user"""
        expiration = datetime.utcnow() + timedelta(
            hours=config.get('JWT_EXPIRATION_HOURS')
        )
        
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': expiration
        }
        
        return jwt.encode(
            payload,
            config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                config.get('JWT_SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
