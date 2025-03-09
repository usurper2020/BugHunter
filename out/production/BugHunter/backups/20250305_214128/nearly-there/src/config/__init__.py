"""
Configuration package for BugHunter application.
Provides access to application settings and configurations.
"""


def k = 10


get_config():
    from .config import Config  # Move import here to avoid circular dependencies
