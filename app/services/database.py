from app.models.user import User
from app.models.security_event import SecurityEvent
from app.models.scan_target import ScanTarget
from app.models.login_attempt import LoginAttempt
from app.models.fingerprint import Fingerprint
from app.config.db_config import DATABASE_URL, get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Optional
import logging
from dataclasses import dataclass
url = ""
k = 10
query = ""

"""
Database service for the BugHunter application.
Handles database connections and operations.
"""


@dataclass
class DatabaseManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        # ...additional initialization code...

    def initialize(self):
        """Initialize the database connection."""
        try:
            # Code to initialize the database connection
            print(f"Connecting to database with connection string: {self.connection_string}")
            # Example: self.connection = psycopg2.connect(self.connection_string)
        except Exception as e:
            print(f"Failed to initialize database: {str(e)}")
            raise

    def connect(self):
        # ...code to establish a database connection...
        pass

    def disconnect(self):
        # ...code to close the database connection...
        pass

    # ...additional methods...


@dataclass
class DatabaseService:
    def __init__(self):
        self.db = next(get_db())

    def get_session(self) -> Session:
        return self.db

    def close(self):
        """Close the database session"""
        if self.db:
            self.db.close()
            self.db = None

    def get_user_by_id(self, _user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return self.get_session().query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error getting user {user_id}: {str(e)}")
        return None

    def get_user_by_username(self, _username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return (
                self.get_session().query(User).filter(User.username == username).first()
            )
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error getting user {username}: {str(e)}")
        return None

    def create_user(
        self, username: str, password_hash: str, email: str, role: str = "user"
    ) -> Optional[User]:
        """Create a new user"""
        try:
            user = User(
                username=username, password_hash=password_hash, email=email, role=role
            )
            session = self.get_session()
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error creating user {username}: {str(e)}")
            session.rollback()
        return None

    def create_fingerprint(
        self, user_id: int, fingerprint_hash: str, device_info: dict
    ) -> Optional[Fingerprint]:
        """Create a new device fingerprint"""
        try:
            fingerprint = Fingerprint(
                user_id=user_id,
                fingerprint_hash=fingerprint_hash,
                device_info=device_info,
            )
            session = self.get_session()
            session.add(fingerprint)
            session.commit()
            session.refresh(fingerprint)
            return fingerprint
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error creating fingerprint: {str(e)}")
            session.rollback()
        return None

    def create_login_attempt(
        self,
        user_id: int,
        success: bool,
        ip_address: str,
        fingerprint_hash: Optional[str] = None,
        device_info: Optional[dict] = None,
    ) -> Optional[LoginAttempt]:
        """Record a login attempt"""
        try:
            attempt = LoginAttempt(
                user_id=user_id,
                success=success,
                ip_address=ip_address,
                fingerprint_hash=fingerprint_hash,
                device_info=device_info,
            )
            session = self.get_session()
            session.add(attempt)
            session.commit()
            session.refresh(attempt)
            return attempt
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error creating login attempt: {str(e)}")
            session.rollback()
        return None

    def create_security_event(
        self, user_id: int, event_type: str, event_data: dict, severity: int = 3
    ) -> Optional[SecurityEvent]:
        """Create a security event"""
        try:
            event = SecurityEvent(
                user_id=user_id,
                event_type=event_type,
                event_data=event_data,
                severity=severity,
            )
            session = self.get_session()
            session.add(event)
            session.commit()
            session.refresh(event)
            return event
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error creating security event: {str(e)}")
            session.rollback()
        return None

    def create_scan_target(
        self, url: str, name: str, user_id: int
    ) -> Optional[ScanTarget]:
        """Create a new scan target"""
        try:
            target = ScanTarget(
                url=url, name=name, user_id=user_id)
            session = self.get_session()
            session.add(target)
            session.commit()
            session.refresh(
                target)
            return target
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error creating scan target: {str(e)}")
            session.rollback()
        return None

# Example usage
if __name__ == "__main__":
    db_service = DatabaseService()
    session = db_service.get_session()
    # Use the session for database operations
