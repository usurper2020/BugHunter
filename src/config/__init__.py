from .base_config import BaseConfig

def load_application_settings():
    """
    Load application settings.

Configuration package for BugHunter application.
Provides access to application settings and configurations.
"""

from .config import Config
from .base_config import BaseConfig


class Config(BaseConfig):
    """
    Configuration class for BugHunter application.
    Extends BaseConfig to allow for future custom configurations.
    """
    pass


if __name__ == "__main__":
    load_application_settings()
