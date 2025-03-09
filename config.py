import os
from pathlib import Path
from typing import Dict, Any
import json
import secrets

class Config:
    """Configuration management for the Bug Hunter application"""
    
    def __init__(self):
        self.config_file = 'config.json'
        self.load_config()
        
    def load_config(self) -> None:
        """Load configuration from environment variables and config file"""
        # Generate a default secret key
        default_secret_key = secrets.token_hex(32)
        
        # Default configuration
        self.config = {
            # Database settings
            'DB_HOST': os.getenv('DB_HOST', 'localhost'),
            'DB_PORT': int(os.getenv('DB_PORT', '5432')),
            'DB_NAME': os.getenv('DB_NAME', 'bughunter'),
            'DB_USER': os.getenv('DB_USER', 'bughunter'),
            'DB_PASSWORD': os.getenv('DB_PASSWORD', ''),
            
            # Security settings
            'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', default_secret_key),
            'JWT_EXPIRATION_HOURS': int(os.getenv('JWT_EXPIRATION_HOURS', '24')),
            'PASSWORD_MIN_LENGTH': int(os.getenv('PASSWORD_MIN_LENGTH', '12')),
            'MAX_LOGIN_ATTEMPTS': int(os.getenv('MAX_LOGIN_ATTEMPTS', '5')),
            'LOGIN_LOCKOUT_MINUTES': int(os.getenv('LOGIN_LOCKOUT_MINUTES', '15')),
            
            # API settings
            'RATE_LIMIT_REQUESTS': int(os.getenv('RATE_LIMIT_REQUESTS', '100')),
            'RATE_LIMIT_WINDOW_MINUTES': int(os.getenv('RATE_LIMIT_WINDOW_MINUTES', '60')),
            
            # Scanning settings
            'MAX_CONCURRENT_SCANS': int(os.getenv('MAX_CONCURRENT_SCANS', '5')),
            'SCAN_TIMEOUT_MINUTES': int(os.getenv('SCAN_TIMEOUT_MINUTES', '30')),
            'DEFAULT_SCAN_DEPTH': os.getenv('DEFAULT_SCAN_DEPTH', 'medium'),
            
            # Report settings
            'REPORT_RETENTION_DAYS': int(os.getenv('REPORT_RETENTION_DAYS', '30')),
            'ENCRYPT_REPORTS': os.getenv('ENCRYPT_REPORTS', 'true').lower() == 'true',
            
            # Logging settings
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'LOG_FILE': os.getenv('LOG_FILE', 'logs/bughunter.log'),
            'LOG_ROTATION_DAYS': int(os.getenv('LOG_ROTATION_DAYS', '7')),
            
            # Cache settings
            'REDIS_HOST': os.getenv('REDIS_HOST', 'localhost'),
            'REDIS_PORT': int(os.getenv('REDIS_PORT', '6379')),
            'CACHE_TTL_MINUTES': int(os.getenv('CACHE_TTL_MINUTES', '60')),
            
            # Tool paths
            'TOOLS_DIRECTORY': os.getenv('TOOLS_DIRECTORY', 'tools'),
            'NUCLEI_TEMPLATES': os.getenv('NUCLEI_TEMPLATES', 'nuclei-templates'),
            
            # AI Integration Settings
            'AI_API_TYPE': os.getenv('AI_API_TYPE', 'codegpt'),
            'AI_API_KEY': os.getenv('AI_API_KEY', ''),
            'AI_MODEL': os.getenv('AI_MODEL', 'gpt-4'),
            'AI_TEMPERATURE': float(os.getenv('AI_TEMPERATURE', '0.7')),
            'AI_CACHE_TTL_MINUTES': int(os.getenv('AI_CACHE_TTL_MINUTES', '60')),
            'AI_MAX_TOKENS': int(os.getenv('AI_MAX_TOKENS', '2000')),
            'AI_ANALYSIS_ENABLED': os.getenv('AI_ANALYSIS_ENABLED', 'true').lower() == 'true',
            
            # Feature flags
            'ENABLE_COLLABORATION': os.getenv('ENABLE_COLLABORATION', 'true').lower() == 'true',
            'ENABLE_ANALYTICS': os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true',
            
            # CodeGPT Widget ID
            'CODEGPT_WIDGET_ID': os.getenv('CODEGPT_WIDGET_ID', '83b8e7bc-6f29-4501-8690-2b1220a9c581')
        }
        
        # Load from config file if it exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in {self.config_file}, using default configuration")
            except Exception as e:
                print(f"Warning: Error reading {self.config_file}: {str(e)}")
                
        # Create necessary directories
        self._create_directories()
        
        # Save the configuration if it doesn't exist
        if not os.path.exists(self.config_file):
            self._save_config()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        directories = [
            'logs',
            'reports',
            'data',
            'cache',
            'tools',
            'templates'
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self.config[key] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save configuration: {str(e)}")
    
    def get_database_url(self) -> str:
        """Get the database URL for SQLAlchemy"""
        return f"postgresql://{self.config['DB_USER']}:{self.config['DB_PASSWORD']}@" \
               f"{self.config['DB_HOST']}:{self.config['DB_PORT']}/{self.config['DB_NAME']}"
    
    def get_redis_url(self) -> str:
        """Get the Redis URL"""
        return f"redis://{self.config['REDIS_HOST']}:{self.config['REDIS_PORT']}/0"

# Create a global instance
config = Config()
