import os
import json
import sys

with open('debug_output.txt', 'w') as f:
    f.write("=== Debug Output ===\n\n")
    
    # Write Python version and encoding
    f.write(f"Python Version: {sys.version}\n")
    f.write(f"File System Encoding: {sys.getfilesystemencoding()}\n\n")
    
    # Write current directory
    f.write(f"Current Directory: {os.getcwd()}\n\n")
    
    # Write environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    f.write(f"OPENAI_API_KEY environment variable: {'Present' if api_key else 'Not found'}\n")
    if api_key:
        f.write(f"API Key value: {api_key[:8]}...\n\n")
    
    # Write config.json contents
    f.write("config.json contents:\n")
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            f.write(json.dumps(config, indent=2))
    except FileNotFoundError:
        f.write("config.json file not found\n")
    except json.JSONDecodeError:
        f.write("config.json is not valid JSON\n")
    except Exception as e:
        f.write(f"Error reading config.json: {str(e)}\n")
    
    f.write("\n\n=== Debug Output Complete ===\n")

print("Debug information has been written to debug_output.txt")
