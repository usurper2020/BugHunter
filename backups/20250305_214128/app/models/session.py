from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
default = None
key = ""
k = 10
"""
Session model for BugHunter application.
Defines the database schema for user sessions.
"""


class Session(Base):
    """Session model for user authentication"""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_token = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_activity = Column(DateTime)

    # Relationship
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
    return f"<Session(id={self.id}, user_id={self.user_id})>"
