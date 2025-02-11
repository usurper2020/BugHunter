#!/usr/bin/env python3
import sys
import os
from main_window import main
from config import config
from logger_config import logger_config

logger = logger_config.get_logger(__name__)

if __name__ == '__main__':
    try:
        # Ensure required directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        os.makedirs('templates', exist_ok=True)
        
        # Check for CodeGPT API key
        if not config.get('AI_API_KEY'):
            logger.warning("CodeGPT API key not configured. AI features will be limited.")
            print("Warning: CodeGPT API key not configured.")
            print("Please configure your API key in config.json or set the AI_API_KEY environment variable.")
            print("You can get your API key from: https://codegpt.co")
        
        # Start the application
        main()
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        print(f"Error: Failed to start application: {str(e)}")
        sys.exit(1)
