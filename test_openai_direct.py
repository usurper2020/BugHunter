from openai import OpenAI
import json

def test_openai():
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
