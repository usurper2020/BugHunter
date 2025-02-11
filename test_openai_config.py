import os
import json
from openai import OpenAI

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {str(e)}")
        return {}

def test_openai_connection():
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
