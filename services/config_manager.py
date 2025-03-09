import json
from pathlib import Path
import logging

class ConfigManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_path = Path('config/config.json')
        self.default_config = {
            "window": {
                "title": "BugHunter",
                "min_width": 800,
                "min_height": 600
            },
            "theme": "dark",
            "update_check": True,
            "api": {
                "timeout": 30,
                "retries": 3
            }
        }

    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if not self.config_path.exists():
                self.config_path.parent.mkdir(exist_ok=True)
                self.save_config(self.default_config)
                return self.default_config

            with open(self.config_path) as f:
                return json.load(f)

        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return self.default_config

    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
