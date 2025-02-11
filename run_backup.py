#!/usr/bin/env python3
import sys
import os
from src.application import main
from src.core import config, logger_config

logger = logger_config.get_logger(__name__)

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['logs', 'data', 'reports', 'templates', 'tools', 'cache']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

if __name__ == '__main__':
    try:
        # Ensure required directories exist
        ensure_directories()
        
        # Check for CodeGPT API key
        if not config.get('AI_API_KEY'):
            logger.warning("CodeGPT API key not configured. AI features will be limited.")
            print("Warning: CodeGPT API key not configured.")
            print("Please configure your API key in config.json or set the AI_API_KEY environment variable.")
            print("You can get your API key from: https://codegpt.co")
        
        # Initialize application
        main()
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        print(f"Error: Failed to start application: {str(e)}")
        sys.exit(1)