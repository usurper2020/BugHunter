import os
import json
from typing import Any, Dict, Optional

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.config_path = os.path.join('config', 'system_config.json')
        self.config_data = {}
        self.load_config()
        self._initialized = True
    
    def load_config(self) -> None:
        """Load configuration from the JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
            else:
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI system configuration"""
        return self.config_data.get('ai_system', {})
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security system configuration"""
        return self.config_data.get('security_system', {})
    
    def get_integration_config(self) -> Dict[str, Any]:
        """Get integration configuration"""
        return self.config_data.get('integration', {})
    
    def get_collaboration_config(self) -> Dict[str, Any]:
        """Get collaboration system configuration"""
        return self.config_data.get('collaboration', {})
    
    def get_tool_config(self) -> Dict[str, Any]:
        """Get tools configuration"""
        return self.config_data.get('tools', {})
    
    def get_analytics_config(self) -> Dict[str, Any]:
        """Get analytics configuration"""
        return self.config_data.get('analytics', {})
    
    def get_middleware_config(self) -> Dict[str, Any]:
        """Get middleware configuration"""
        return self.config_data.get('middleware', {})
    
    def get_config_value(self, section: str, key: str, default: Any = None) -> Any:
        """Get a specific configuration value"""
        try:
            return self.config_data[section][key]
        except KeyError:
            return default
    
    def update_config(self, section: str, key: str, value: Any) -> None:
        """Update a specific configuration value"""
        if section not in self.config_data:
            self.config_data[section] = {}
        
        self.config_data[section][key] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save the current configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving configuration: {str(e)}")
