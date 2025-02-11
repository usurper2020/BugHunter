import os
from openai import OpenAI

def test_openai_connection():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
        
        # Test API connection
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
