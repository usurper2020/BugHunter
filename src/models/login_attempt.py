"""
LoginAttempt model for BugHunter application.
Defines the database schema for login attempts.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, String

from sqlalchemy.orm import relationship
from src.models.base import Base

class LoginAttempt(Base):
    """LoginAttempt model for tracking user login attempts"""
    __tablename__ = 'login_attempts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    attempt_time = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))

    # Relationship
    user = relationship("User", back_populates="login_attempts")

    def __repr__(self):
        return f"<LoginAttempt(id={self.id}, user_id={self.user_id})>"
