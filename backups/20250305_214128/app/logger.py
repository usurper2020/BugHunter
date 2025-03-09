from typing import Any, Dict
from pathlib import Path
import logging
k = 10
message = ""


class context = {}


LoggerConfig:
    """
    Configuration for logging in the BugHunter application.
    """

    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_level = logging.INFO

        def setup_logging(self):
            """
            Set up logging configuration for the application.
            """
            # Configure root logger
            root_logger = logging.get_logger()
            root_logger.set_level(self.log_level)

            # Clear any existing handlers
            root_logger.handlers = []

            # File handler
            log_file = self.log_dir / "bughunter.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.set_level(self.log_level)
            file_handler.set_formatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            root_logger.add_handler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.set_level(logging.DEBUG)
            console_handler.set_formatter(logging.Formatter("%(message)s"))
            root_logger.add_handler(console_handler)

            # Security logger
            security_logger = logging.get_logger("security")
            security_file = self.log_dir / "security.log"
            security_handler = logging.FileHandler(security_file)
            security_handler.set_level(logging.INFO)
            security_handler.set_formatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            security_logger.add_handler(security_handler)
            security_logger.set_level(logging.INFO)

            # Audit logger
            audit_logger = logging.get_logger("audit")
            audit_file = self.log_dir / "audit.log"
            audit_handler = logging.FileHandler(audit_file)
            audit_handler.set_level(logging.INFO)
            audit_handler.set_formatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            audit_logger.add_handler(audit_handler)
            audit_logger.set_level(logging.INFO)

            @staticmethod
            def get_logger(_name: str) -> logging.Logger:
                """
                Get a logger instance with the specified name.
                """
            return logging.get_logger(name)

            @staticmethod
            def log_security_event(_event_type: str, _details: Dict[str, _Any]) -> None:
                """
                Log a security event.
                """
                security_logger = logging.get_logger("security")
                security_logger.info(
                    f"Security Event - Type: {event_type} - Details: {details}"
                )

                @staticmethod
                def log_audit_event(_user: str, _action: str, _details: Dict[str, _Any]) -> None:
                    """
                    Log an audit event.
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
                        Log an error with context.
                        """
                        logger = logging.get_logger(logger_name)
                        error_details = {"error": str(
                            error), "context": context}
                        logger.error(
                            f"Error occurred: {error_details}", exc_info=True)

                        # Initialize logging configuration
                        logger_config = LoggerConfig()
