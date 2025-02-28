"""
Session model for BugHunter application.
Defines the database schema for user sessions.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base

class Session(Base):
    """Session model for user authentication"""
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_token = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_activity = Column(DateTime)

    # Relationship
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id})>"
