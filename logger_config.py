import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from config import config

class LoggerConfig:
    """
    Configure and manage logging for the BugHunter application.
    
    This class provides comprehensive logging configuration including:
    - File-based logging with rotation
    - Console output
    - Separate security and audit logging
    - Error tracking with context
    
    The logging system supports multiple log levels and specialized
    loggers for different types of events (security, audit, etc.).
    """
    
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
        """
        Convert string log level to corresponding logging constant.
        
        Maps configuration string values to logging module constants:
        - DEBUG -> logging.DEBUG (10)
        - INFO -> logging.INFO (20)
        - WARNING -> logging.WARNING (30)
        - ERROR -> logging.ERROR (40)
        - CRITICAL -> logging.CRITICAL (50)
        
        Returns:
            int: The numeric logging level (defaults to INFO if invalid)
        """
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    
    def _configure_logging(self) -> None:
        """
        Configure the logging system with all necessary handlers.
        
        Sets up:
        - Root logger with file and console handlers
        - Security logger for security-related events
        - Audit logger for user actions
        
        Each logger is configured with:
        - Appropriate log level from configuration
        - File rotation at midnight
        - Consistent formatting across all handlers
        - Separate log files for different concerns
        """
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
        """
        Get a configured logger instance for a specific module.
        
        Parameters:
            name (str): The name for the logger, typically __name__
                       of the calling module
                       
        Returns:
            logging.Logger: A configured logger instance that inherits
                          the root logger's configuration
        """
        return logging.getLogger(name)
    
    @staticmethod
    def log_security_event(event_type: str, details: Dict[str, Any]) -> None:
        """
        Log a security-related event to the security log.
        
        Parameters:
            event_type (str): Type of security event (e.g., 'login_attempt',
                            'permission_change')
            details (Dict[str, Any]): Additional details about the event,
                                    such as usernames, IP addresses, etc.
        """
        security_logger = logging.getLogger('security')
        security_logger.info(f"Security Event - Type: {event_type} - Details: {details}")
    
    @staticmethod
    def log_audit_event(user: str, action: str, details: Dict[str, Any]) -> None:
        """
        Log a user action for audit purposes.
        
        Parameters:
            user (str): Username of the person performing the action
            action (str): Description of the action performed
            details (Dict[str, Any]): Additional context about the action,
                                    such as affected resources, parameters, etc.
        """
        audit_logger = logging.getLogger('audit')
        audit_logger.info(
            f"Audit Event - User: {user} - Action: {action} - Details: {details}"
        )
    
    @staticmethod
    def log_error(logger_name: str, error: Exception, context: Dict[str, Any] = None) -> None:
        """
        Log an error with additional context information.
        
        Parameters:
            logger_name (str): Name of the logger to use
            error (Exception): The exception that occurred
            context (Dict[str, Any], optional): Additional context about
                                              the error, such as operation
                                              being performed, relevant IDs, etc.
                                              
        The error log includes:
        - Error type and message
        - Timestamp of occurrence
        - Stack trace
        - Any provided context
        """
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
# try:
#     # Some code that might raise an exception
#     raise ValueError("Example error")
# except Exception as e:
#     logger_config.log_error(__name__, e, {"operation": "example_operation"})
