"""
Configuration management service for the BugHunter application.
Handles loading, saving, and accessing application configurations.
"""

import json
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """Manages application configuration settings"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.ConfigManager')
        self.config: Dict[str, Any] = {}
        self.config_dir = Path('config')
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self, filename: str) -> bool:
        """Load configuration from file"""
        try:
            file_path = Path(filename)
            if not file_path.is_absolute():
                file_path = self.config_dir / file_path
            
            if not file_path.exists():
                self.logger.warning(f"Configuration file not found: {file_path}")
                return False
            
            with open(file_path, 'r') as f:
                if file_path.suffix == '.json':
                    config_data = json.load(f)
                elif file_path.suffix in ['.yml', '.yaml']:
                    config_data = yaml.safe_load(f)
                else:
                    self.logger.error(f"Unsupported configuration format: {file_path.suffix}")
                    return False
            
            self.config.update(config_data)
            self.logger.info(f"Configuration loaded: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration {filename}: {str(e)}")
            return False
    
    def save_config(self, filename: str) -> bool:
        """Save current configuration to file"""
        try:
            file_path = Path(filename)
            if not file_path.is_absolute():
                file_path = self.config_dir / file_path
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                if file_path.suffix == '.json':
                    json.dump(self.config, f, indent=4)
                elif file_path.suffix in ['.yml', '.yaml']:
                    yaml.safe_dump(self.config, f)
                else:
                    self.logger.error(f"Unsupported configuration format: {file_path.suffix}")
                    return False
            
            self.logger.info(f"Configuration saved: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration {filename}: {str(e)}")
            return False
    
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration setting"""
        try:
            return self.config.get(section, {}).get(key, default)
        except Exception as e:
            self.logger.error(f"Error retrieving setting {section}.{key}: {str(e)}")
            return default
    
    def set_setting(self, section: str, key: str, value: Any) -> bool:
        """Set a configuration setting"""
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            return True
        except Exception as e:
            self.logger.error(f"Error setting {section}.{key}: {str(e)}")
            return False
    
    def get_window_state(self) -> Optional[bytes]:
        """Get saved window state"""
        try:
            return self.get_setting('window', 'state')
        except Exception as e:
            self.logger.error(f"Error retrieving window state: {str(e)}")
            return None
    
    def save_window_state(self, state: bytes) -> bool:
        """Save window state"""
        try:
            return self.set_setting('window', 'state', state)
        except Exception as e:
            self.logger.error(f"Error saving window state: {str(e)}")
            return False
