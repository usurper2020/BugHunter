# scripts/verify_env.py
import os
from dotenv import load_dotenv
import openai

def verify_environment():
    """Verify environment setup and API keys"""
    print("Verifying environment setup...")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        return False
    
    # Load environment variables
    load_dotenv(override=True)
    
    # Check OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file!")
        return False
    
    print(f"Found API key: {api_key[:6]}...{api_key[-4:]}")
    
    # Verify OpenAI API key
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="test",
            max_tokens=5
        )
        print("OpenAI API key verified successfully!")
        return True
    except Exception as e:
        print(f"Error verifying OpenAI API key: {e}")
        return False

if __name__ == "__main__":
    verify_environment()
