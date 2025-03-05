# tests/test_codebreaker.py
from unittest import TestCase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..src.codebreaker import CodeBreaker

# Use actual implementation
def test_codebreaker():
    from ..src.codebreaker import CodeBreaker
    # Test implementation
# src/config/base_config.py
from pathlib import Path
from typing import Dict, Any, Optional
import os

class BaseConfig:
    """Base configuration class for the BugHunter application."""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / 'src'
    TESTS_DIR = BASE_DIR / 'tests'
    UTILS_DIR = BASE_DIR / 'utils'
    
    # Database configuration
    DATABASE = {
        'driver': 'sqlite',
        'name': 'bughunter.db',
        'path': str(BASE_DIR / 'data'),
    }
    
    # Logging configuration
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': str(BASE_DIR / 'logs' / 'bughunter.log'),
                'mode': 'a',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default', 'file'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }
    
    # AI configuration
    AI_CONFIG = {
        'model_path': str(BASE_DIR / 'models'),
        'max_tokens': 1000,
        'temperature': 0.7
    }
    
    # Testing configuration
    TEST_CONFIG = {
        'test_data_path': str(TESTS_DIR / 'data'),
        'mock_responses': str(TESTS_DIR / 'mock_responses')
    }
    
    @classmethod
    def get_db_url(cls) -> str:
        """Generate database URL from configuration."""
        return f"{cls.DATABASE['driver']}:///{os.path.join(cls.DATABASE['path'], cls.DATABASE['name'])}"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        directories = [
            cls.DATABASE['path'],
            os.path.dirname(cls.LOGGING['handlers']['file']['filename']),
            cls.AI_CONFIG['model_path'],
            cls.TEST_CONFIG['test_data_path'],
            cls.TEST_CONFIG['mock_responses']
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_config_value(cls, key: str, default: Any = None) -> Any:
        """Safely get configuration value."""
        return getattr(cls, key, default)
    
    @classmethod
    def update_config(cls, updates: Dict[str, Any]) -> None:
        """Update configuration values."""
        for key, value in updates.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

    @classmethod
    def get_alembic_config(cls) -> Dict[str, Any]:
        """Get Alembic-specific configuration."""
        return {
            'script_location': 'alembic',
            'sqlalchemy.url': cls.get_db_url(),
            'file_template': '%%(year)d%%(month).2d%%(day).2d_%%(rev)s_%%(slug)s'
        }

