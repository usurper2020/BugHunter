from pathlib import Path
import secrets
import os
import json
from typing import Any

"""
Configuration management for BugHunter application.
Handles loading and accessing configuration settings.
"""

class Config:
    """Configuration management"""

    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if not self.config_path.exists():
            self.create_default_config()

        with open(self.config_path, encoding="utf-8") as f:
            self.config = json.load(f)

    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "database": {
                "DB_HOST": os.getenv("DB_HOST", "localhost"),
                "DB_PORT": os.getenv("DB_PORT", 5432),
                "DB_NAME": os.getenv("DB_NAME", "bughunter_logincredentials"),
                "DB_USER": os.getenv("DB_USER", "postgres"),
                "DB_PASSWORD": os.getenv("DB_PASSWORD", "your-secure-password-here"),
                "ADMIN_USER": "admin",
                "ADMIN_PASSWORD": "StrongPassword123!",
            },
            "security": {
                "JWT_SECRET_KEY": secrets.token_hex(32),
                "JWT_EXPIRATION_HOURS": 24,
                "PASSWORD_MIN_LENGTH": 12,
                "MAX_LOGIN_ATTEMPTS": 5,
                "LOGIN_LOCKOUT_MINUTES": 15,
            },
            "logging": {
                "LOG_LEVEL": "INFO",
                "LOG_FILE": "logs/bughunter.log",
                "LOG_ROTATION_DAYS": 7,
            },
            "spacy": {
                "model": "en_core_web_sm",
            },
        }

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)

    def get(self, _key: str, _default=None) -> Any:
        """Get configuration value"""
        keys = _key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return _default

# Create global config instance
config = Config()

# Export DATABASE_URL for SQLAlchemy
DATABASE_URL = f"postgresql://{config.get('database.DB_USER')}:{config.get('database.DB_PASSWORD')}@{config.get('database.DB_HOST')}:{config.get('database.DB_PORT')}/{config.get('database.DB_NAME')}"

# Export ADMIN_CREDENTIALS
ADMIN_CREDENTIALS = {
    "username": config.get("database.ADMIN_USER"),
    "password": config.get("database.ADMIN_PASSWORD"),
}
