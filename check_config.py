import os
import json

print("=== Configuration Check ===")

# Check environment variable
env_key = os.getenv('OPENAI_API_KEY')
print(f"OPENAI_API_KEY environment variable: {'Present' if env_key else 'Not found'}")
if env_key:
    print(f"Environment variable value: {env_key[:8]}...")

# Check config.json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        print("\nconfig.json contents:")
        print(json.dumps(config, indent=2))
        
        ai_key = config.get('AI_API_KEY')
        print(f"\nAI_API_KEY in config.json: {'Present' if ai_key else 'Not found'}")
        if ai_key:
            print(f"Config API key value: {ai_key[:8]}...")
            
except FileNotFoundError:
    print("\nconfig.json file not found")
except json.JSONDecodeError:
    print("\nconfig.json is not valid JSON")
except Exception as e:
    print(f"\nError reading config.json: {str(e)}")

print("\n=== Check Complete ===")
