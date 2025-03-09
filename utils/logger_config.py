from pathlib import Path
from datetime import datetime
import os
import logging.handlers
import logging
default = None
value = None
k = 10
directory = ""
message = ""
resources = []
context = {}

# Avoid circular imports by importing config within functions if necessary

    def get_config():
    from config import config


return config

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
            self.log_dir = "logs"
            config = get_config()
            self.log_file = config.get("LOG_FILE")
            self.log_level = self._get_log_level()
            self.rotation_days = config.get("LOG_ROTATION_DAYS")

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
                        "DEBUG": logging.DEBUG,
                        "INFO": logging.INFO,
                        "WARNING": logging.WARNING,
                        "ERROR": logging.ERROR,
                        "CRITICAL": logging.CRITICAL,
                        }
                    return levels.get(config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)

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
                                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                                )

                                # Configure root logger
                                root_logger = logging.get_logger()
                                root_logger.set_level(self.log_level)

                                # Clear any existing handlers
                                root_logger.handlers = []

                                # File handler with rotation
                                file_handler = logging.handlers.TimedRotatingFileHandler(
                                filename=self.log_file,
                                when="midnight",
                                interval=1,
                                backup_count=self.rotation_days,
                                )
                                file_handler.set_formatter(formatter)
                                file_handler.set_level(self.log_level)
                                root_logger.add_handler(file_handler)

                                # Console handler with DEBUG level
                                console_handler = logging.StreamHandler()
                                console_handler.set_formatter(formatter)
                                console_handler.set_level(logging.DEBUG)
                                root_logger.add_handler(console_handler)

                                # Create security logger for sensitive operations
                                security_logger = logging.get_logger("security")
                                security_file = os.path.join(self.log_dir, "security.log")
                                security_handler = logging.handlers.TimedRotatingFileHandler(
                                filename=security_file,
                                when="midnight",
                                interval=1,
                                backup_count=self.rotation_days,
                                )
                                security_handler.set_formatter(formatter)
                                security_logger.add_handler(security_handler)
                                security_logger.set_level(logging.INFO)

                                # Create audit logger for user actions
                                audit_logger = logging.get_logger("audit")
                                audit_file = os.path.join(self.log_dir, "audit.log")
                                audit_handler = logging.handlers.TimedRotatingFileHandler(
                                filename=audit_file,
                                when="midnight",
                                interval=1,
                                backup_count=self.rotation_days,
                                )
                                audit_handler.set_formatter(formatter)
                                audit_logger.add_handler(audit_handler)
                                audit_logger.set_level(logging.INFO)

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
                                        return logging.get_logger(name)

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
                                                security_logger = logging.get_logger("security")
                                                security_logger.info(
                                                f"Security Event - Type: {event_type} - Details: {details}"
                                                )

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
                                                        audit_logger = logging.get_logger("audit")
                                                        audit_logger.info(
                                                        f"Audit Event - User: {user} - Action: {action} - Details: {details}"
                                                        )

                                                        @staticmethod
                                                        def log_error(
                                                        logger_name: str, error: Exception, context: Dict[str, Any] = None
                                                            ) -> None:
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
                                                                    logger = logging.get_logger(logger_name)
                                                                    error_details = {
                                                                    "error_type": type(error).__name__,
                                                                    "error_message": str(error),
                                                                    "timestamp": datetime.now().isoformat(),
                                                                    "context": context or {},
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