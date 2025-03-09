from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON

default = None
key = ""
k = 10

"""
SecurityEvent model for BugHunter application.
Defines the database schema for security events.
"""

class SecurityEvent(Base):
    """SecurityEvent model for tracking security-related events"""

    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSON)
    severity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    # Relationship
    user = relationship("User", back_populates="security_events")

    def __repr__(self):
        return f"<SecurityEvent(id={self.id}, type={self.event_type})>"
