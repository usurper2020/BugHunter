import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from src import config

class LoggerConfig:
    """Configure logging for the Bug Hunter application"""
    
    def __init__(self):
        self.log_dir = 'logs'
        self.log_file = config.get('LOG_FILE')
        self.log_level = self._get_log_level()
        self.rotation_days = config.get('LOG_ROTATION_DAYS')
        
        # Create logs directory if it doesn't exist
        Path(self.log_dir).mkdir(exist_ok=True)
        
        # Configure logging
        self._configure_logging()
    
    def _get_log_level(self) -> int:
        """Convert string log level to logging constant"""
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    
    def _configure_logging(self) -> None:
        """Configure logging with file and console handlers"""
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        root_logger.handlers = []
        
        # File handler with rotation
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_file,
            when='midnight',
            interval=1,
            backupCount=self.rotation_days
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.log_level)
        root_logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        root_logger.addHandler(console_handler)
        
        # Create security logger for sensitive operations
        security_logger = logging.getLogger('security')
        security_file = os.path.join(self.log_dir, 'security.log')
        security_handler = logging.handlers.TimedRotatingFileHandler(
            filename=security_file,
            when='midnight',
            interval=1,
            backupCount=self.rotation_days
        )
        security_handler.setFormatter(formatter)
        security_logger.addHandler(security_handler)
        security_logger.setLevel(logging.INFO)
        
        # Create audit logger for user actions
        audit_logger = logging.getLogger('audit')
        audit_file = os.path.join(self.log_dir, 'audit.log')
        audit_handler = logging.handlers.TimedRotatingFileHandler(
            filename=audit_file,
            when='midnight',
            interval=1,
            backupCount=self.rotation_days
        )
        audit_handler.setFormatter(formatter)
        audit_logger.addHandler(audit_handler)
        audit_logger.setLevel(logging.INFO)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger instance with the specified name"""
        return logging.getLogger(name)
    
    @staticmethod
    def log_security_event(event_type: str, details: Dict[str, Any]) -> None:
        """Log a security event"""
        security_logger = logging.getLogger('security')
        security_logger.info(f"Security Event - Type: {event_type} - Details: {details}")
    
    @staticmethod
    def log_audit_event(user: str, action: str, details: Dict[str, Any]) -> None:
        """Log an audit event"""
        audit_logger = logging.getLogger('audit')
        audit_logger.info(
            f"Audit Event - User: {user} - Action: {action} - Details: {details}"
        )
    
    @staticmethod
    def log_error(logger_name: str, error: Exception, context: Dict[str, Any] = None) -> None:
        """Log an error with context"""
        logger = logging.getLogger(logger_name)
        error_details = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        logger.error(f"Error occurred: {error_details}", exc_info=True)

# Initialize logging configuration
logger_config = LoggerConfig()

# Example usage:
# logger = logger_config.get_logger(__name__)
# logger.info("Application started")
# logger_config.log_security_event("login_attempt", {"username": "user1", "success": True})
# logger_config.log_audit_event("user1", "scan_started", {"target": "example.com"})
