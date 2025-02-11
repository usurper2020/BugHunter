from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from database import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class ScanStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SeverityLevel(enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_login = Column(DateTime)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)

    # Relationships
    scan_results = relationship("ScanResult", back_populates="created_by_user")
    reports = relationship("Report", back_populates="created_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class ScanResult(Base):
    __tablename__ = 'scan_results'

    id = Column(Integer, primary_key=True)
    scan_id = Column(String(50), unique=True, nullable=False)
    target_url = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    status = Column(Enum(ScanStatus), nullable=False, default=ScanStatus.PENDING)
    created_by = Column(Integer, ForeignKey('users.id'))
    total_findings = Column(Integer, default=0)

    # Relationships
    created_by_user = relationship("User", back_populates="scan_results")
    findings = relationship("Finding", back_populates="scan_result")
    reports = relationship("Report", back_populates="scan_result")

    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'target_url': self.target_url,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status.value,
            'created_by': self.created_by,
            'total_findings': self.total_findings
        }

class Finding(Base):
    __tablename__ = 'findings'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scan_results.id'))
    type = Column(String(50), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    description = Column(Text, nullable=False)
    details = Column(Text)
    discovered_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    scan_result = relationship("ScanResult", back_populates="findings")

    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'type': self.type,
            'severity': self.severity.value,
            'description': self.description,
            'details': self.details,
            'discovered_at': self.discovered_at.isoformat()
        }

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    report_id = Column(String(50), unique=True, nullable=False)
    scan_id = Column(Integer, ForeignKey('scan_results.id'))
    format = Column(String(10), nullable=False)
    file_path = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    encrypted = Column(Boolean, default=False)
    encryption_key = Column(Text)

    # Relationships
    scan_result = relationship("ScanResult", back_populates="reports")
    created_by_user = relationship("User", back_populates="reports")

    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'scan_id': self.scan_id,
            'format': self.format,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by,
            'encrypted': self.encrypted
        }

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    ip_address = Column(String(45))
    details = Column(JSON)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address,
            'details': self.details
        }

class ScanSchedule(Base):
    __tablename__ = 'scan_schedules'

    id = Column(Integer, primary_key=True)
    target_url = Column(Text, nullable=False)
    frequency = Column(String(20), nullable=False)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'target_url': self.target_url,
            'frequency': self.frequency,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'created_by': self.created_by,
            'active': self.active,
            'created_at': self.created_at.isoformat()
        }

class RateLimit(Base):
    __tablename__ = 'rate_limits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    endpoint = Column(String(100), nullable=False)
    requests_count = Column(Integer, default=0)
    window_start = Column(DateTime, nullable=False, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'endpoint': self.endpoint,
            'requests_count': self.requests_count,
            'window_start': self.window_start.isoformat()
        }
