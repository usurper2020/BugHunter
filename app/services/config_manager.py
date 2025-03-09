from pathlib import Path
import logging
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass
value = None
key = ""
k = 10

"""
Configuration Manager for BugHunter application.
Handles loading and managing application configuration.
"""


@dataclass
class ConfigManager:
    """Handles application configuration"""

    def __init__(self, config_file):
        self.logger = logging.get_logger("BugHunter.ConfigManager")
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file {self.config_file} not found.")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {self.config_file}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error loading config: {e}")
            return {}

    def get_config(self, key: Optional[str] = None) -> Any:
        """
        Get configuration value(s)

        Args:
            key: Optional specific configuration key to retrieve

        Returns:
            The requested configuration value(s)
        """
        try:
            if key:
                return self.config.get(key)
            return self.config
        except Exception as e:
            self.logger.error(f"Error getting config: {str(e)}")
            return None

    def set_config(self, key: str, value: Any) -> bool:
        """
        Set a configuration value

        Args:
            key: Configuration key to set
            value: Value to set

        Returns:
            True if successful, False otherwise
        """
        try:
            self.config[key] = value
            self.save_config(self.config)
            return True
        except Exception as e:
            self.logger.error(f"Error setting config: {str(e)}")
            return False

    def save_config(self, config) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error saving config: {e}")
            return False