# Core package initialization and global instances
from src.config import Config
from src.logger import LoggerConfig

# Create global instances
config = Config()
logger_config = LoggerConfig()

# Export instances for easy access
__all__ = ['config', 'logger_config']
