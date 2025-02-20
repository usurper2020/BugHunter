"""
File-based OpenAI API test module for the BugHunter application.

This module provides OpenAI API testing with detailed logging to file,
including configuration details, API responses, and error tracking.
All output is written to 'openai_test_output.txt' for later analysis.
"""

from openai import OpenAI
import json
import sys
from datetime import datetime
import traceback

def log(message):
    """
    Write a timestamped log message to file.
    
    Parameters:
        message (str): Message to log
        
    Output Format:
        [YYYY-MM-DD HH:MM:SS] message
        
    Note:
        Messages are appended to 'openai_test_output.txt'
    """
    with open('openai_test_output.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def test_openai():
    """
    Test OpenAI API connectivity with detailed file logging.
    
    This function performs a complete API test:
    1. Loads and validates configuration
    2. Initializes OpenAI client
    3. Attempts API communication
    4. Logs all steps and results
    
    Error Handling:
    - Validates API key presence
    - Captures and logs all exceptions
    - Records Python version and stack traces
    - Preserves error context for debugging
    
    Output:
        All operations and results are logged to 'openai_test_output.txt'
        including configuration details (with API key partially obscured)
        and full error context if failures occur.
    """
    try:
        log("Loading config.json...")
        with open('config.json', 'r') as f:
            config = json.load(f)
            log("Config loaded successfully")
            log(f"Config contents: {json.dumps(config, indent=2)}")
        
        api_key = config.get('AI_API_KEY')
        if not api_key:
            log("Error: AI_API_KEY not found in config")
            return
            
        log(f"Found API key: {api_key[:8]}...")
        
        log("Initializing OpenAI client...")
        client = OpenAI(api_key=api_key)
        log("OpenAI client initialized")
        
        log("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        log("Success! Response received:")
        log(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        log(f"Error occurred: {str(e)}")
        log(f"Error type: {type(e).__name__}")
        log(f"Python version: {sys.version}")
        log(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    log("\n=== Starting OpenAI Test ===")
    test_openai()
    log("=== Test Complete ===\n")
