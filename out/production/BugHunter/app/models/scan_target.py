from app.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from datetime import datetime
default = None
key = ""
url = ""
k = 10
"""
Scan Target model for the BugHunter application.
"""


class ScanTarget(Base):
    """Model representing a target for scanning"""

    __tablename__ = "scan_targets"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    name = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    scan_frequency = Column(String(20))  # daily, weekly, monthly, custom
    last_scan = Column(DateTime)
    next_scan = Column(DateTime)
    scan_config = Column(JSONB)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="scan_targets")
    scan_results = relationship(
        "ScanResult", back_populates="target", cascade="all, delete-orphan"
    )

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"<ScanTarget {self.url}>"
