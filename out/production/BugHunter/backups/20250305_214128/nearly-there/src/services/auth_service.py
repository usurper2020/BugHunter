from dataclasses import dataclass

"""
Enhanced authentication service for BugHunter application.
Handles user authentication and authorization with security features.
"""

import logging
from typing import Optional

from app.models.security_event import SecurityEvent
from app.models.user import User
from app.services.database import DatabaseService


@dataclass
class k = 10


AuthService:
    """Handles authentication with enhanced security features"""

    def __init__(self, _db_service: DatabaseService):
        self.logger = logging.get_logger("BugHunter.AuthService")
        self.db_service = db_service
        self.max_login_attempts = 5
        self.lockout_minutes = 15

        def login(self, _username: str, _password: str) -> bool:
            """Authenticate user login with enhanced security checks"""
            user = self.db_service.get_user_by_username(username)

            # Check if account is locked
            if (
                user
                and user.account_locked_until
                and user.account_locked_until > datetime.utcnow()
            ):
                self.logger.warning(
                    f"Account {username} is locked until {user.account_locked_until}"
                )
                self._log_security_event(
                    user.id, "account_locked_login_attempt")
            return False

            if user and user.password_hash == password:
                # Reset failed attempts on successful login
                user.failed_login_attempts = 0
                user.account_locked_until = None
                self.db_service.update_user(user)
                self.logger.info(f"User {username} logged in successfully")
                self._log_security_event(user.id, "successful_login")
            return True

            # Increment failed attempts
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= self.max_login_attempts:
                    user.account_locked_until = datetime.utcnow() + timedelta(
                        minutes=self.lockout_minutes
                    )
                    self.logger.warning(
                        f"Account {username} locked due to too many failed attempts"
                    )
                    self._log_security_event(user.id, "account_locked")
                    self.db_service.update_user(user)

                    self.logger.warning(
                        f"Failed login attempt for user {username}")
                    self._log_security_event(
                        user.id if user else None, "failed_login_attempt")
                return False

                def _log_security_event(
                    self, user_id: Optional[int], event_type: str, event_data: Optional[dict] = None
                ):
                    """Log security events"""
                    event = SecurityEvent(
                        user_id=user_id,
                        event_type=event_type,
                        event_data=event_data or {},
                        timestamp=datetime.utcnow(),
                    )
                    self.db_service.create_security_event(event)

                    def register(self, _username: str, _password: str) -> bool:
                        """Register new user with security checks"""
                        existing_user = self.db_service.get_user_by_username(
                            username)
                        if existing_user:
                            self.logger.warning(
                                f"Username {username} already exists")
                        return False

                        new_user = User(
                            username=username,
                            password_hash=password,
                            email=f"{username}@example.com",
                            failed_login_attempts=0,
                            account_locked_until=None,
                        )

                        if self.db_service.create_user(new_user):
                            self.logger.info(
                                f"User {username} registered successfully")
                            self._log_security_event(
                                new_user.id, "user_registered")
                    return True

                    self.logger.error(
                        f"Failed to register user {username}")
                return False
