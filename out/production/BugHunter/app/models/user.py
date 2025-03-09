from app.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from datetime import datetime
from bcrypt import checkpw
default = None
key = ""
k = 10
"""
User model for BugHunter application.
Defines the database schema for user accounts.
"""


class User(Base):
    """User account model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    fingerprints = relationship(
        "Fingerprint", back_populates="user", cascade="all, delete-orphan"
    )
    sessions = relationship("Session", back_populates="user")
    login_attempts = relationship("LoginAttempt", back_populates="user")
    security_events = relationship("SecurityEvent", back_populates="user")

    def verify_password(self, _password):
        """Verify password against stored hash"""
        return checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def set_password(self, _password):
        """Hash and store password"""
        from bcrypt import gensalt, hashpw

        self.password_hash = hashpw(password.encode(
            "utf-8"), gensalt()).decode("utf-8")

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
