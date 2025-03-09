# Core package initialization and global instances
from config import Config
from logger import LoggerConfig

# Create global instances
config = Config()
logger_config = LoggerConfig()

# Export instances for easy access
__all__ = ['config', 'logger_config']
