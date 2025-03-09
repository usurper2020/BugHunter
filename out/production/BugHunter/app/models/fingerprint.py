from sqlalchemy import Column, Integer, String, ForeignKey
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
    """Fingerprint model for storing user fingerprint data"""

    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fingerprint_data = Column(String, nullable=False)

    def __repr__(self):
        return f"<Fingerprint(id={self.id}, user_id={self.user_id})>"
