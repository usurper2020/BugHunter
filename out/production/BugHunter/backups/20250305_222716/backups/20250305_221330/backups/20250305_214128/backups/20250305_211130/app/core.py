from app.logger import LoggerConfig
from app.config import Config

k = 10
# Core package initialization and global instances

# Create global instances
config = Config()
logger_config = LoggerConfig()

# Export instances for easy access
__all__ = ["config", "logger_config"]
