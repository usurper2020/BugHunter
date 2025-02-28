from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from models.user import User, Fingerprint, Session as UserSession, LoginAttempt, SecurityEvent
from datetime import datetime
import json
from typing import Optional, List, Dict, Any

class DatabaseService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def close(self):
        """Close the database session"""
        self.db.close()

    # User Operations
    def create_user(self, username: str, password_hash: str, email: str, 
                   first_name: str = None, last_name: str = None, role: str = 'user') -> User:
        """Create a new user"""
        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            created_at=datetime.utcnow(),
            is_active=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user_last_login(self, user_id: int) -> None:
        """Update user's last login time"""
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit()

    def increment_failed_login(self, user_id: int) -> None:
        """Increment failed login attempts for user"""
        user = self.get_user_by_id(user_id)
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:  # Lock account after 5 failed attempts
                user.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
            self.db.commit()

    def reset_failed_login_attempts(self, user_id: int) -> None:
        """Reset failed login attempts counter"""
        user = self.get_user_by_id(user_id)
        if user:
            user.failed_login_attempts = 0
            user.account_locked_until = None
            self.db.commit()

    # Fingerprint Operations
    def create_fingerprint(self, user_id: int, fingerprint_hash: str, 
                         device_info: dict, ip_address: str = None) -> Fingerprint:
        """Create a new device fingerprint"""
        fingerprint = Fingerprint(
            user_id=user_id,
            fingerprint_hash=fingerprint_hash,
            device_info=device_info,
            ip_address=ip_address,
            created_at=datetime.utcnow(),
            last_used=datetime.utcnow(),
            is_active=True,
            trust_score=50  # Default middle trust score
        )
        self.db.add(fingerprint)
        self.db.commit()
        self.db.refresh(fingerprint)
        return fingerprint

    def get_fingerprint(self, fingerprint_hash: str) -> Optional[Fingerprint]:
        """Get fingerprint by hash"""
        return self.db.query(Fingerprint).filter(
            Fingerprint.fingerprint_hash == fingerprint_hash
        ).first()

    def update_fingerprint_trust_score(self, fingerprint_hash: str, score: int) -> None:
        """Update trust score for a fingerprint"""
        fingerprint = self.get_fingerprint(fingerprint_hash)
        if fingerprint:
            fingerprint.trust_score = max(0, min(100, score))  # Ensure score is 0-100
            fingerprint.last_used = datetime.utcnow()
            self.db.commit()

    # Session Operations
    def create_session(self, user_id: int, session_token: str, fingerprint_hash: str,
                      ip_address: str = None, user_agent: str = None) -> UserSession:
        """Create a new user session"""
        session = UserSession(
            user_id=user_id,
            session_token=session_token,
            fingerprint_hash=fingerprint_hash,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=7),
            last_activity=datetime.utcnow(),
            is_active=True,
            ip_address=ip_address,
            user_agent=user_agent,
            session_data={}
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_active_session(self, session_token: str) -> Optional[UserSession]:
        """Get active session by token"""
        return self.db.query(UserSession).filter(
            and_(
                UserSession.session_token == session_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            )
        ).first()

    def invalidate_session(self, session_token: str, reason: str = None) -> None:
        """Invalidate a session"""
        session = self.get_active_session(session_token)
        if session:
            session.is_active = False
            session.revocation_reason = reason
            self.db.commit()

    def update_session_activity(self, session_token: str) -> None:
        """Update last activity time for session"""
        session = self.get_active_session(session_token)
        if session:
            session.last_activity = datetime.utcnow()
            self.db.commit()

    # Login Attempt Operations
    def create_login_attempt(self, user_id: int, success: bool, ip_address: str,
                           fingerprint_hash: str = None, device_info: dict = None,
                           attempt_type: str = 'password', failure_reason: str = None,
                           geolocation: dict = None) -> LoginAttempt:
        """Record a login attempt"""
        attempt = LoginAttempt(
            user_id=user_id,
            ip_address=ip_address,
            attempt_time=datetime.utcnow(),
            success=success,
            fingerprint_hash=fingerprint_hash,
            device_info=device_info,
            attempt_type=attempt_type,
            failure_reason=failure_reason,
            geolocation=geolocation,
            risk_score=self._calculate_risk_score(success, device_info, ip_address)
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get_recent_login_attempts(self, user_id: int, limit: int = 5) -> List[LoginAttempt]:
        """Get recent login attempts for user"""
        return self.db.query(LoginAttempt).filter(
            LoginAttempt.user_id == user_id
        ).order_by(desc(LoginAttempt.attempt_time)).limit(limit).all()

    # Security Event Operations
    def create_security_event(self, user_id: int, event_type: str, event_data: dict,
                            ip_address: str = None, fingerprint_hash: str = None,
                            severity: int = 3) -> SecurityEvent:
        """Create a new security event"""
        event = SecurityEvent(
            user_id=user_id,
            event_type=event_type,
            event_time=datetime.utcnow(),
            event_data=event_data,
            ip_address=ip_address,
            fingerprint_hash=fingerprint_hash,
            severity=severity,
            is_resolved=False
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def resolve_security_event(self, event_id: int, resolution_notes: str) -> None:
        """Mark a security event as resolved"""
        event = self.db.query(SecurityEvent).get(event_id)
        if event:
            event.is_resolved = True
            event.resolution_notes = resolution_notes
            event.resolution_time = datetime.utcnow()
            self.db.commit()

    def _calculate_risk_score(self, success: bool, device_info: dict, 
                            ip_address: str) -> int:
        """Calculate risk score for login attempt"""
        score = 50  # Base score
        
        if not success:
            score += 20  # Failed attempts are riskier
        
        # Add more risk calculation logic based on device_info and ip_address
        # This is a placeholder implementation
        return min(100, max(0, score))  # Ensure score is between 0-100
