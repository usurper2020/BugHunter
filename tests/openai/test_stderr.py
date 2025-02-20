from openai import OpenAI
import json
import sys
from datetime import datetime

def write_error(message):
    sys.stderr.write(f"{message}\n")
    sys.stderr.flush()
    with open('error_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def test_openai():
    try:
        write_error("\n=== Starting OpenAI Test ===")
        
        # Load config
        write_error("Loading config.json...")
        with open('config.json', 'r') as f:
            config = json.load(f)
        write_error("Config loaded successfully")
        
        # Get API key
        api_key = config.get('AI_API_KEY')
        if not api_key:
            write_error("Error: AI_API_KEY not found in config")
            return
        write_error(f"Found API key: {api_key[:8]}...")
        
        # Initialize client
        write_error("Initializing OpenAI client...")
        client = OpenAI(api_key=api_key)
        write_error("OpenAI client initialized")
        
        # Test API
        write_error("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a different model as a test
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            temperature=0.7
        )
        write_error("Success! Response received:")
        write_error(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        write_error(f"Error occurred: {str(e)}")
        write_error(f"Error type: {type(e).__name__}")
        write_error(f"Python version: {sys.version}")
        import traceback
        write_error(f"Traceback: {traceback.format_exc()}")
    
    write_error("=== Test Complete ===\n")

if __name__ == "__main__":
    test_openai()
