import os
import json
from openai import OpenAI
from datetime import datetime

def print_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def load_config():
    try:
        print_log("Attempting to load config.json...")
        with open('config.json', 'r') as f:
            config = json.load(f)
            print_log("Successfully loaded config.json")
            print_log(f"Config contents: {json.dumps(config, indent=2)}")
            return config
    except Exception as e:
        print_log(f"Error loading config.json: {str(e)}")
        return {}

def test_openai_connection():
    print_log("Starting OpenAI connection test")
    
    # Try getting API key from config.json first
    config = load_config()
    api_key = config.get('AI_API_KEY', '')
    print_log(f"API Key from config.json: {'Found' if api_key else 'Not found'}")
    
    # If not found in config, try environment variable
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        print_log(f"API Key from environment: {'Found' if api_key else 'Not found'}")
    
    if not api_key:
        print_log("No API key found in either config.json or environment variables")
        return
    
    try:
        # Initialize OpenAI client
        print_log(f"Attempting to initialize OpenAI client with API key: {api_key[:8]}...")
        client = OpenAI(api_key=api_key)
        print_log("OpenAI client initialized successfully")
        
        # Test API connection
        print_log("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        print_log("API test successful!")
        print_log(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print_log(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    print_log("\n=== Starting new test run ===")
    test_openai_connection()
    print_log("=== Test run completed ===\n")
