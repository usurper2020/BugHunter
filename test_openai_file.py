from openai import OpenAI
import json
import sys
from datetime import datetime

def log(message):
    with open('openai_test_output.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def test_openai():
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
        import traceback
        log(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    log("\n=== Starting OpenAI Test ===")
    test_openai()
    log("=== Test Complete ===\n")
