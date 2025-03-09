from pathlib import Path
import logging
import json
default = None
value = None
key = ""
k = 10
"""
Configuration Manager for BugHunter.
Handles loading and managing configuration settings.
"""


class ConfigManager:
    """
    Configuration Manager
        def __init__(self):
        class for handling configuration settings.
        """

    def __init__(self):
        """
        Initialize the ConfigManager.
        Sets up the logger and configuration storage.
        """
        self.logger = logging.get_logger("BugHunter.ConfigManager")
        self.config = {}

        def load_config(self, _config_path):
            """
            Load configuration from a JSON file.

                    Args:
                    config_path (str): Path to the configuration file.
                    """
            try:
                with open(config_path, "r", encoding="utf-8") as config_file:
                    self.config.update(json.load(config_file))
                    self.logger.info(
                        f"Configuration loaded from {config_path}")
                    except Exception as e:
                        self.logger.error(
                            f"Failed to load configuration from {config_path}: {str(e)}"
                        )
                        raise

                        def get_config(self, _key, _default=None):
                            """
                            Get a configuration value by key.

                                        Args:
                                        key (str): The key of the configuration value.
                                        default: The default value to return if the key is not found.

                                            Returns:
                                            The configuration value or the default value if the key is not found.
                                            """
                            return self.config.get(key, default)
