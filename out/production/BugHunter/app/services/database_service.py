from app.models.user import User
from app.models.security_event import SecurityEvent
from app.models.scan_target import ScanTarget
from app.models.login_attempt import LoginAttempt
from app.models.fingerprint import Fingerprint
from app.config.db_config import DATABASE_URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from typing import Optional
from dataclasses import dataclass
import logging
url = ""
k = 10
query = ""


@dataclass
class DatabaseService:
    def __init__(self, _config_manager):
        self.logger = logging.get_logger("BugHunter.DatabaseService")
        self.config_manager = config_manager
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.session: Optional[Session] = None

        def get_session(self) -> Session:
            """Get a database session"""
            if not self.session:
                self.session = self.SessionLocal()
            return self.session

            def close(self):
                """Close the database session"""
                if self.session:
                    self.session.close()
                    self.session = None

                    # Validation Methods
                    def validate_user_data(self, _username: str, _email: str) -> bool:
                        """Validate user data"""
                        if not username or not email:
                            return False
                        if "@" not in email:
                            return False
                        return True

                    def validate_fingerprint_data(
                        self, fingerprint_hash: str, device_info: dict
                    ) -> bool:
                        """Validate fingerprint data"""
                        if not fingerprint_hash or not device_info:
                        return False
                    return True

                    def validate_login_attempt_data(self, _ip_address: str) -> bool:
                        """Validate login attempt data"""
                        if not ip_address:
                        return False
                    return True

                    def validate_security_event_data(self, _event_type: str, _event_data: dict) -> bool:
                        """Validate security event data"""
                        if not event_type or not event_data:
                        return False
                    return True

                    def validate_scan_target_data(self, _url: str, _name: str) -> bool:
                        """Validate scan target data"""
                        if not url or not name:
                        return False
                    return True

                    # User Methods
                    def create_user(
                        self, username: str, password_hash: str, email: str, role: str = "user"
                    ) -> Optional[User]:
                        """Create a new user"""
                        if not self.validate_user_data(username, email):
                            self.logger.error(
                                f"Invalid user data: username={username}, email={email}")
                        return None
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

                        def update_user(self, _user: User) -> bool:
                            """Update user details"""
                            if not self.validate_user_data(user.username, user.email):
                                self.logger.error(
                                    f"Invalid user data: username={user.username}, email={user.email}"
                                )
                            return False
                            try:
                                session = self.get_session()
                                session.merge(user)
                                session.commit()
                            return True
                            except SQLAlchemyError as e:
                                self.logger.error(
                                    f"Database error updating user {user.id}: {str(e)}")
                                session.rollback()
                            return False

                            def delete_user(self, _user_id: int) -> bool:
                                """Delete a user by their ID"""
                                try:
                                    session = self.get_session()
                                    user = session.query(User).filter(
                                        User.id == user_id).first()
                                    if user:
                                        session.delete(user)
                                        session.commit()
                                    return True
                                    else:
                                        self.logger.error(
                                            f"User with ID {user_id} not found")
                                    return False
                                    except SQLAlchemyError as e:
                                        self.logger.error(
                                            f"Database error deleting user {user_id}: {str(e)}")
                                        session.rollback()
                                    return False

                                    def get_user_by_id(self, _user_id: int) -> Optional[User]:
                                        """Retrieve a user by their ID"""
                                        try:
                                            session = self.get_session()
                                            user = session.query(User).filter(
                                                User.id == user_id).first()
                                        return user
                                        except SQLAlchemyError as e:
                                            self.logger.error(
                                                f"Database error retrieving user {user_id}: {str(e)}")
                                        return None

                                        # Fingerprint Methods
                                        def create_fingerprint(
                                            self, user_id: int, fingerprint_hash: str, device_info: dict
                                        ) -> Optional[Fingerprint]:
                                            """Create a new device fingerprint"""
                                            if not self.validate_fingerprint_data(fingerprint_hash, device_info):
                                                self.logger.error(
                                                    f"Invalid fingerprint data: fingerprint_hash={fingerprint_hash}, device_info={device_info}"
                                                )
                                            return None
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

                                            def delete_fingerprint(self, _fingerprint_id: int) -> bool:
                                                """Delete a fingerprint by its ID"""
                                                try:
                                                    session = self.get_session()
                                                    fingerprint = (
                                                        session.query(
                                                            Fingerprint)
                                                        .filter(Fingerprint.id == fingerprint_id)
                                                        .first()
                                                    )
                                                    if fingerprint:
                                                        session.delete(
                                                            fingerprint)
                                                        session.commit()
                                                    return True
                                                    else:
                                                        self.logger.error(
                                                            f"Fingerprint with ID {fingerprint_id} not found")
                                                    return False
                                                    except SQLAlchemyError as e:
                                                        self.logger.error(
                                                            f"Database error deleting fingerprint {fingerprint_id}: {str(e)}"
                                                        )
                                                        session.rollback()
                                                    return False

                                                    # Login Attempt Methods
                                                    def create_login_attempt(
                                                        self,
                                                        user_id: int,
                                                        success: bool,
                                                        ip_address: str,
                                                        fingerprint_hash: Optional[str] = None,
                                                        device_info: Optional[dict] = None,
                                                    ) -> Optional[LoginAttempt]:
                                                        """Record a login attempt"""
                                                        if not self.validate_login_attempt_data(ip_address):
                                                            self.logger.error(
                                                                f"Invalid login attempt data: ip_address={ip_address}")
                                                        return None
                                                        try:
                                                            attempt = LoginAttempt(
                                                                user_id=user_id,
                                                                success=success,
                                                                ip_address=ip_address,
                                                                fingerprint_hash=fingerprint_hash,
                                                                device_info=device_info,
                                                            )
                                                            session = self.get_session()
                                                            session.add(
                                                                attempt)
                                                            session.commit()
                                                            session.refresh(
                                                                attempt)
                                                        return attempt
                                                        except SQLAlchemyError as e:
                                                            self.logger.error(
                                                                f"Database error creating login attempt: {str(e)}")
                                                            session.rollback()
                                                        return None

                                                        def delete_login_attempt(self, _attempt_id: int) -> bool:
                                                            """Delete a login attempt by its ID"""
                                                            try:
                                                                session = self.get_session()
                                                                attempt = (
                                                                    session.query(
                                                                        LoginAttempt)
                                                                    .filter(LoginAttempt.id == attempt_id)
                                                                    .first()
                                                                )
                                                                if attempt:
                                                                    session.delete(
                                                                        attempt)
                                                                    session.commit()
                                                                return True
                                                                else:
                                                                    self.logger.error(
                                                                        f"Login attempt with ID {attempt_id} not found")
                                                                return False
                                                                except SQLAlchemyError as e:
                                                                    self.logger.error(
                                                                        f"Database error deleting login attempt {attempt_id}: {str(e)}"
                                                                    )
                                                                    session.rollback()
                                                                return False

                                                                # Security Event Methods
                                                                def create_security_event(
                                                                    self, user_id: int, event_type: str, event_data: dict, severity: int = 3
                                                                ) -> Optional[SecurityEvent]:
                                                                    """Create a security event"""
                                                                    if not self.validate_security_event_data(event_type, event_data):
                                                                        self.logger.error(
                                                                            f"Invalid security event data: event_type={event_type}, event_data={event_data}"
                                                                        )
                                                                    return None
                                                                    try:
                                                                        event = SecurityEvent(
                                                                            user_id=user_id,
                                                                            event_type=event_type,
                                                                            event_data=event_data,
                                                                            severity=severity,
                                                                        )
                                                                        session = self.get_session()
                                                                        session.add(
                                                                            event)
                                                                        session.commit()
                                                                        session.refresh(
                                                                            event)
                                                                    return event
                                                                    except SQLAlchemyError as e:
                                                                        self.logger.error(
                                                                            f"Database error creating security event: {str(e)}")
                                                                        session.rollback()
                                                                    return None

                                                                    def delete_security_event(self, _event_id: int) -> bool:
                                                                        """Delete a security event by its ID"""
                                                                        try:
                                                                            session = self.get_session()
                                                                            event = (
                                                                                session.query(
                                                                                    SecurityEvent)
                                                                                .filter(SecurityEvent.id == event_id)
                                                                                .first()
                                                                            )
                                                                            if event:
                                                                                session.delete(
                                                                                    event)
                                                                                session.commit()
                                                                            return True
                                                                            else:
                                                                                self.logger.error(
                                                                                    f"Security event with ID {event_id} not found")
                                                                            return False
                                                                            except SQLAlchemyError as e:
                                                                                self.logger.error(
                                                                                    f"Database error deleting security event {event_id}: {str(e)}"
                                                                                )
                                                                                session.rollback()
                                                                            return False

                                                                            # Scan Target Methods
                                                                            def create_scan_target(
                                                                                self, url: str, name: str, user_id: int
                                                                            ) -> Optional[ScanTarget]:
                                                                                """Create a new scan target"""
                                                                                try:
                                                                                    target = ScanTarget(
                                                                                        url=url, name=name, user_id=user_id)
                                                                                    session = self.get_session()
                                                                                    session.add(
                                                                                        target)
                                                                                    session.commit()
                                                                                    session.refresh(
                                                                                        target)
                                                                                return target
                                                                                except SQLAlchemyError as e:
                                                                                    self.logger.error(
                                                                                        f"Database error creating scan target: {str(e)}")
                                                                                    session.rollback()
                                                                                return None

                                                                                def update_scan_target(self, _target: ScanTarget) -> bool:
                                                                                    """Update scan target details"""
                                                                                    if not self.validate_scan_target_data(target.url, target.name):
                                                                                        self.logger.error(
                                                                                            f"Invalid scan target data: url={target.url}, name={target.name}"
                                                                                        )
                                                                                    return False
                                                                                    try:
                                                                                        session = self.get_session()
                                                                                        session.merge(
                                                                                            target)
                                                                                        session.commit()
                                                                                    return True
                                                                                    except SQLAlchemyError as e:
                                                                                        self.logger.error(
                                                                                            f"Database error updating scan target {target.id}: {str(e)}"
                                                                                        )
                                                                                        session.rollback()
                                                                                    return False

                                                                                    def delete_scan_target(self, _target_id: int) -> bool:
                                                                                        """Delete a scan target by its ID"""
                                                                                        try:
                                                                                            session = self.get_session()
                                                                                            target = (
                                                                                                session.query(ScanTarget).filter(
                                                                                                    ScanTarget.id == target_id).first()
                                                                                            )
                                                                                            if target:
                                                                                                session.delete(
                                                                                                    target)
                                                                                                session.commit()
                                                                                            return True
                                                                                            else:
                                                                                                self.logger.error(
                                                                                                    f"Scan target with ID {target_id} not found")
                                                                                            return False
                                                                                            except SQLAlchemyError as e:
                                                                                                self.logger.error(
                                                                                                    f"Database error deleting scan target {target_id}: {str(e)}"
                                                                                                )
                                                                                                session.rollback()
                                                                                            return False
