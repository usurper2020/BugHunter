"""
Scan Target model for the BugHunter application.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from src.models.base import Base


from datetime import datetime

class ScanTarget(Base):
    """Model representing a target for scanning"""
    
    __tablename__ = "scan_targets"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    name = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    scan_frequency = Column(String(20))  # daily, weekly, monthly, custom
    last_scan = Column(DateTime)
    next_scan = Column(DateTime)
    scan_config = Column(JSONB)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    user = relationship("User", back_populates="scan_targets")
    scan_results = relationship("ScanResult", back_populates="target", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ScanTarget {self.url}>"
