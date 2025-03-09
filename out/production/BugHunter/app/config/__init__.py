from .base_config import BaseConfig
from .config import Config


k = 10


def load_application_settings():
    """
    Load application settings.

    Configuration package for BugHunter application.
    Provides access to application settings and configurations."""

    class Config(BaseConfig):
        """
        Configuration class for BugHunter application.
        Extends BaseConfig to allow for future custom configurations.
        """

    pass

    if __name__ == "__main__":
        load_application_settings()
