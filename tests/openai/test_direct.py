"""
Direct OpenAI API test module for the BugHunter application.

This module provides a simple, direct test of OpenAI API functionality
without additional logging or error handling layers. Used for basic
connectivity verification and troubleshooting.
"""

from openai import OpenAI
import json

def test_openai():
    """
    Perform a basic test of OpenAI API connectivity.
    
    This function:
    1. Loads API key from config.json
    2. Initializes OpenAI client
    3. Sends a test message to verify API functionality
    
    The test uses a simple chat completion request with
    minimal configuration. API key is partially obscured
    in console output for security.
    
    Note:
        Requires valid API key in config.json
        Prints progress and results to console
    """
    print("Loading config.json...")
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    api_key = config.get('AI_API_KEY')
    print(f"Found API key: {api_key[:8]}...")
    
    print("Initializing OpenAI client...")
    client = OpenAI(api_key=api_key)
    
    print("Testing API connection...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        print("Success! Response received:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("=== Starting OpenAI Test ===")
    test_openai()
    print("=== Test Complete ===")
