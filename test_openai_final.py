from openai import OpenAI
import json
import sys
from datetime import datetime
import os

def log_and_print(message):
    print(message)  # Print to console
    log_dir = 'logs'
    log_file = os.path.join(log_dir, 'openai_test.log')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    with open(log_file, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def test_openai():
    try:
        log_and_print("\n=== Starting OpenAI Test ===")
        
        # Load config
        log_and_print("Loading config.json...")
        with open('config.json', 'r') as f:
            config = json.load(f)
        log_and_print("Config loaded successfully")
        
        # Get API key
        api_key = config.get('AI_API_KEY')
        if not api_key:
            log_and_print("Error: AI_API_KEY not found in config")
            return
        log_and_print(f"Found API key: {api_key[:8]}...")
        
        # Initialize client
        log_and_print("Initializing OpenAI client...")
        client = OpenAI(api_key=api_key)
        log_and_print("OpenAI client initialized")
        
        # Test API
        log_and_print("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a different model as a test
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        log_and_print("Success! Response received:")
        log_and_print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        log_and_print(f"Error occurred: {str(e)}")
        log_and_print(f"Error type: {type(e).__name__}")
        log_and_print(f"Python version: {sys.version}")
        import traceback
        log_and_print(f"Traceback: {traceback.format_exc()}")
    
    log_and_print("=== Test Complete ===\n")

if __name__ == "__main__":
    test_openai()
