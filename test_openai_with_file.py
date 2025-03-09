import os
import json
from openai import OpenAI
from datetime import datetime

def write_log(message):
    with open('openai_test.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def load_config():
    try:
        write_log("Attempting to load config.json...")
        with open('config.json', 'r') as f:
            config = json.load(f)
            write_log("Successfully loaded config.json")
            return config
    except Exception as e:
        write_log(f"Error loading config.json: {str(e)}")
        return {}

def test_openai_connection():
    write_log("Starting OpenAI connection test")
    
    # Try getting API key from config.json first
    config = load_config()
    api_key = config.get('AI_API_KEY', '')
    write_log(f"API Key from config.json: {'Found' if api_key else 'Not found'}")
    
    # If not found in config, try environment variable
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        write_log(f"API Key from environment: {'Found' if api_key else 'Not found'}")
    
    if not api_key:
        write_log("No API key found in either config.json or environment variables")
        return
    
    try:
        # Initialize OpenAI client
        write_log(f"Attempting to initialize OpenAI client with API key: {api_key[:8]}...")
        client = OpenAI(api_key=api_key)
        write_log("OpenAI client initialized successfully")
        
        # Test API connection
        write_log("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        write_log("API test successful!")
        write_log(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        write_log(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    write_log("\n=== Starting new test run ===")
    test_openai_connection()
    write_log("=== Test run completed ===\n")
