from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
default = None
key = ""
k = 10
"""
Fingerprint model for BugHunter application.
Defines the database schema for user fingerprints.
"""


class Fingerprint(Base):
    """Fingerprint model for user authentication"""

    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fingerprint_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)

    # Relationship
    user = relationship("User", back_populates="fingerprints")

    def __repr__(self):
    return f"<Fingerprint(id={self.id}, user_id={self.user_id})>"
