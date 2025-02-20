from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from database import Base

class UserRole(enum.Enum):
    """
    Enumeration of user roles in the system.
    
    Values:
        ADMIN: Full system access and management capabilities
        USER: Standard user with normal access privileges
        VIEWER: Read-only access to system resources
    """
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class ScanStatus(enum.Enum):
    """
    Enumeration of possible scan states.
    
    Values:
        PENDING: Scan is queued but not yet started
        RUNNING: Scan is currently in progress
        COMPLETED: Scan has finished successfully
        FAILED: Scan encountered an error and stopped
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SeverityLevel(enum.Enum):
    """
    Enumeration of vulnerability severity levels.
    
    Values:
        CRITICAL: Severe vulnerabilities requiring immediate attention
        HIGH: Important security issues that should be addressed quickly
        MEDIUM: Moderate security concerns
        LOW: Minor security issues
        INFO: Informational findings without direct security impact
    """
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class User(Base):
    """
    SQLAlchemy model representing a user in the system.
    
    This model stores user authentication and authorization data,
    including password hashes, roles, and login history. It also
    maintains relationships with scan results, reports, and audit logs.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username
        password_hash (str): Hashed password
        role (UserRole): User's role in the system
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        last_login (datetime): Last successful login timestamp
        login_attempts (int): Count of failed login attempts
        locked_until (datetime): Account lock expiration time
        
    Relationships:
        scan_results: One-to-many relationship with ScanResult
        reports: One-to-many relationship with Report
        audit_logs: One-to-many relationship with AuditLog
    """
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
        """
        Convert the User model instance to a dictionary.
        
        Returns:
            dict: User data with the following keys:
                - id: User's unique identifier
                - username: User's username
                - role: User's role value
                - created_at: Account creation timestamp (ISO format)
                - last_login: Last login timestamp (ISO format or None)
        """
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class ScanResult(Base):
    """
    SQLAlchemy model representing a security scan result.
    
    Stores information about security scans including target,
    status, and findings count. Links to the user who created
    the scan and maintains relationships with findings and reports.
    
    Attributes:
        id (int): Primary key
        scan_id (str): Unique identifier for the scan
        target_url (str): URL or target that was scanned
        timestamp (datetime): When the scan was initiated
        status (ScanStatus): Current status of the scan
        created_by (int): Foreign key to users table
        total_findings (int): Total number of findings from the scan
        
    Relationships:
        created_by_user: Many-to-one relationship with User
        findings: One-to-many relationship with Finding
        reports: One-to-many relationship with Report
    """
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
        """
        Convert the ScanResult model instance to a dictionary.
        
        Returns:
            dict: Scan result data with the following keys:
                - id: Scan result unique identifier
                - scan_id: Unique scan identifier
                - target_url: URL that was scanned
                - timestamp: Scan timestamp (ISO format)
                - status: Current scan status value
                - created_by: ID of user who created the scan
                - total_findings: Number of findings from the scan
        """
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
    """
    SQLAlchemy model representing a security finding.
    
    Stores detailed information about vulnerabilities and issues
    discovered during security scans. Each finding is associated
    with a specific scan result.
    
    Attributes:
        id (int): Primary key
        scan_id (int): Foreign key to scan_results table
        type (str): Type of vulnerability found
        severity (SeverityLevel): Severity level of the finding
        description (str): Detailed description of the finding
        details (str): Additional technical details
        discovered_at (datetime): When the finding was discovered
        
    Relationships:
        scan_result: Many-to-one relationship with ScanResult
    """
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
        """
        Convert the Finding model instance to a dictionary.
        
        Returns:
            dict: Finding data with the following keys:
                - id: Finding unique identifier
                - scan_id: ID of associated scan
                - type: Type of vulnerability
                - severity: Severity level value
                - description: Finding description
                - details: Additional technical details
                - discovered_at: Discovery timestamp (ISO format)
        """
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
    """
    SQLAlchemy model representing a scan report.
    
    Manages generated reports from scan results, including
    file information and optional encryption details.
    
    Attributes:
        id (int): Primary key
        report_id (str): Unique identifier for the report
        scan_id (int): Foreign key to scan_results table
        format (str): Report format (e.g., 'pdf', 'html')
        file_path (str): Path to the report file
        created_at (datetime): Report generation timestamp
        created_by (int): Foreign key to users table
        encrypted (bool): Whether the report is encrypted
        encryption_key (str): Optional encryption key
        
    Relationships:
        scan_result: Many-to-one relationship with ScanResult
        created_by_user: Many-to-one relationship with User
    """
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
        """
        Convert the Report model instance to a dictionary.
        
        Returns:
            dict: Report data with the following keys:
                - id: Report unique identifier
                - report_id: Unique report identifier
                - scan_id: ID of associated scan
                - format: Report format
                - created_at: Creation timestamp (ISO format)
                - created_by: ID of user who created the report
                - encrypted: Whether the report is encrypted
        """
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
    """
    SQLAlchemy model representing system audit logs.
    
    Tracks user actions and system events for security
    and compliance purposes. Stores detailed information
    about each action including IP addresses and timestamps.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to users table
        action (str): Description of the action performed
        entity_type (str): Type of entity affected
        entity_id (int): ID of the affected entity
        timestamp (datetime): When the action occurred
        ip_address (str): IP address of the actor
        details (JSON): Additional contextual information
        
    Relationships:
        user: Many-to-one relationship with User
    """
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
        """
        Convert the AuditLog model instance to a dictionary.
        
        Returns:
            dict: Audit log data with the following keys:
                - id: Log entry unique identifier
                - user_id: ID of user who performed the action
                - action: Description of the action
                - entity_type: Type of affected entity
                - entity_id: ID of affected entity
                - timestamp: Action timestamp (ISO format)
                - ip_address: Actor's IP address
                - details: Additional JSON details
        """
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
    """
    SQLAlchemy model representing scheduled scans.
    
    Manages recurring security scans, tracking their frequency
    and execution history. Enables automated scanning of targets
    at specified intervals.
    
    Attributes:
        id (int): Primary key
        target_url (str): URL or target to scan
        frequency (str): How often to run the scan
        last_run (datetime): Last execution timestamp
        next_run (datetime): Next scheduled execution
        created_by (int): Foreign key to users table
        active (bool): Whether the schedule is active
        created_at (datetime): When the schedule was created
    """
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
        """
        Convert the ScanSchedule model instance to a dictionary.
        
        Returns:
            dict: Schedule data with the following keys:
                - id: Schedule unique identifier
                - target_url: URL to be scanned
                - frequency: Scan frequency
                - last_run: Last execution timestamp (ISO format or None)
                - next_run: Next execution timestamp (ISO format or None)
                - created_by: ID of user who created the schedule
                - active: Whether the schedule is active
                - created_at: Creation timestamp (ISO format)
        """
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
    """
    SQLAlchemy model representing API rate limits.
    
    Tracks API usage per user and endpoint to enforce
    rate limiting policies. Helps prevent abuse and
    ensure fair resource utilization.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to users table
        endpoint (str): API endpoint being tracked
        requests_count (int): Number of requests made
        window_start (datetime): Start of current time window
    """
    __tablename__ = 'rate_limits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    endpoint = Column(String(100), nullable=False)
    requests_count = Column(Integer, default=0)
    window_start = Column(DateTime, nullable=False, default=func.now())

    def to_dict(self):
        """
        Convert the RateLimit model instance to a dictionary.
        
        Returns:
            dict: Rate limit data with the following keys:
                - id: Rate limit unique identifier
                - user_id: ID of associated user
                - endpoint: API endpoint being tracked
                - requests_count: Number of requests made
                - window_start: Time window start (ISO format)
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'endpoint': self.endpoint,
            'requests_count': self.requests_count,
            'window_start': self.window_start.isoformat()
        }
