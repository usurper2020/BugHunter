"""
Debug information writer for the BugHunter application.

This script generates a comprehensive debug output file containing:
- Python environment information
- System configuration details
- API key presence verification
- Configuration file contents

The output is written to 'debug_output.txt' for troubleshooting.
"""

import os
import json
import sys

def write_system_info(file):
    """
    Write system and Python environment information.
    
    Parameters:
        file: File object to write to
        
    Writes:
        - Python version
        - File system encoding
        - Current working directory
    """
    file.write("=== Debug Output ===\n\n")
    file.write(f"Python Version: {sys.version}\n")
    file.write(f"File System Encoding: {sys.getfilesystemencoding()}\n\n")
    file.write(f"Current Directory: {os.getcwd()}\n\n")

def write_api_key_info(file):
    """
    Write OpenAI API key presence information.
    
    Parameters:
        file: File object to write to
        
    Writes:
        - Whether API key environment variable exists
        - First 8 characters of key if present (for verification)
        
    Note:
        Full API key is never written for security.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    file.write(f"OPENAI_API_KEY environment variable: {'Present' if api_key else 'Not found'}\n")
    if api_key:
        file.write(f"API Key value: {api_key[:8]}...\n\n")

def write_config_info(file):
    """
    Write configuration file contents.
    
    Parameters:
        file: File object to write to
        
    Writes:
        - Contents of config.json if present
        - Error message if file is missing or invalid
        
    Handles:
        - FileNotFoundError
        - JSONDecodeError
        - Other potential exceptions
    """
    file.write("config.json contents:\n")
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            file.write(json.dumps(config, indent=2))
    except FileNotFoundError:
        file.write("config.json file not found\n")
    except json.JSONDecodeError:
        file.write("config.json is not valid JSON\n")
    except Exception as e:
        file.write(f"Error reading config.json: {str(e)}\n")

def main():
    """
    Main function to generate debug output file.
    
    Creates debug_output.txt containing all debug information
    in a structured format. Handles file operations and
    coordinates the writing of different information sections.
    """
    with open('debug_output.txt', 'w') as f:
        write_system_info(f)
        write_api_key_info(f)
        write_config_info(f)
        f.write("\n\n=== Debug Output Complete ===\n")
    
    print("Debug information has been written to debug_output.txt")

if __name__ == '__main__':
    main()
