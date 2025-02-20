"""
OpenAI API configuration test module for the BugHunter application.

This module verifies the OpenAI API configuration and connectivity by:
- Loading API key from configuration or environment
- Testing API key validity
- Verifying API response functionality

Used for ensuring proper setup of OpenAI integration.
"""

import os
import json
from openai import OpenAI

def load_config():
    """
    Load configuration from config.json file.
    
    Returns:
        dict: Configuration dictionary if successful,
              empty dictionary if file not found or invalid.
              
    Note:
        Prints error message if config file cannot be loaded.
    """
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {str(e)}")
        return {}

def test_openai_connection():
    """
    Test OpenAI API connectivity and functionality.
    
    This function:
    1. Attempts to load API key from config.json
    2. Falls back to environment variable if needed
    3. Initializes OpenAI client
    4. Tests API with a simple chat completion request
    
    The test sends a simple message and verifies response,
    printing status updates throughout the process.
    
    Note:
        Prints detailed status messages and any errors encountered.
        API key is partially obscured in logs for security.
    """
    # Try getting API key from config.json first
    config = load_config()
    api_key = config.get('AI_API_KEY', '')
    print(f"API Key from config.json: {'Yes' if api_key else 'No'}")
    
    # If not found in config, try environment variable
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"API Key from environment: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("No API key found in either config.json or environment variables")
        return
    
    try:
        # Initialize OpenAI client
        print(f"Attempting to initialize OpenAI client with API key: {api_key[:8]}...")
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
        
        # Test API connection
        print("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        print("API test successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_openai_connection()
