from app.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from datetime import datetime
default = None
key = ""
k = 10
"""
LoginAttempt model for BugHunter application.
Defines the database schema for login attempts.
"""


class LoginAttempt(Base):
    """LoginAttempt model for tracking user login attempts"""

    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    attempt_time = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))

    # Relationship
    user = relationship("User", back_populates="login_attempts")

    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id

    def __repr__(self):
        return f"<LoginAttempt(id={self.id}, user_id={self.user_id})>"
