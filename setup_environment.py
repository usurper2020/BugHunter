#!/usr/bin/env python3
import os
import json
import secrets
import sys

def generate_secret_key():
    """
    Generate a cryptographically secure secret key.
    
    Returns:
        str: A 64-character hexadecimal string suitable for use
             as a secret key in cryptographic operations.
    """
    return secrets.token_hex(32)

def create_directories():
    """
    Create required application directories if they don't exist.
    
    Creates the following directories:
    - logs: For application log files
    - tools: For security testing tools
    - reports: For scan reports and output
    - cache: For temporary data storage
    
    Each directory is created with appropriate permissions,
    and existing directories are preserved.
    """
    directories = ['logs', 'tools', 'reports', 'cache']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_config():
    """
    Create default configuration file if it doesn't exist.
    
    Creates config.json with default settings including:
    - API keys (placeholders)
    - JWT configuration
    - Database settings
    - Logging configuration
    - Directory paths
    - Application settings
    
    Note:
        Does not overwrite existing configuration file to
        preserve user settings.
    """
    config_path = 'config.json'
    if not os.path.exists(config_path):
        config = {
            "AI_API_KEY": "your-openai-api-key",
            "SHODAN_API_KEY": "",
            "JWT_SECRET_KEY": generate_secret_key(),
            "JWT_EXPIRATION_HOURS": 24,
            "DB_HOST": "localhost",
            "DB_PORT": 5432,
            "DB_NAME": "bughunter",
            "DB_USER": "bughunter",
            "DB_PASSWORD": "",
            "LOG_LEVEL": "INFO",
            "LOG_FILE": "logs/bughunter.log",
            "TOOLS_DIRECTORY": "tools",
            "REPORTS_DIRECTORY": "reports",
            "CACHE_DIRECTORY": "cache",
            "MAX_CONCURRENT_SCANS": 5,
            "SCAN_TIMEOUT_MINUTES": 30,
            "DEFAULT_SCAN_DEPTH": "medium",
            "ENABLE_COLLABORATION": True,
            "ENABLE_ANALYTICS": True
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created default {config_path}")
    else:
        print(f"{config_path} already exists")

def check_python_version():
    """
    Verify that Python version meets requirements.
    
    Checks if the current Python version is 3.7 or higher,
    which is required for application functionality.
    
    Raises:
        SystemExit: If Python version is below 3.7, exits
                   with status code 1.
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"Python version {version.major}.{version.minor}.{version.micro} OK")

def check_dependencies():
    """
    Verify that all required Python packages are installed.
    
    Reads requirements from requirements.txt and checks if
    they are installed in the current environment.
    
    Raises:
        SystemExit: If any required packages are missing,
                   exits with status code 1 and displays
                   installation instructions.
    """
    try:
        import pkg_resources
        with open('requirements.txt', 'r') as f:
            required = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
        installed = [pkg.key for pkg in pkg_resources.working_set]
        missing = []
        
        for package in required:
            name = package.split('>=')[0].split('==')[0]
            if name.lower() not in [pkg.lower() for pkg in installed]:
                missing.append(package)
                
        if missing:
            print("Missing required packages:")
            for package in missing:
                print(f"  - {package}")
            print("\nInstall missing packages with:")
            print("pip install -r requirements.txt")
            sys.exit(1)
        else:
            print("All required packages are installed")
    except Exception as e:
        print(f"Error checking dependencies: {str(e)}")
        sys.exit(1)

def main():
    """
    Main entry point for environment setup.
    
    Performs complete environment setup:
    1. Verifies Python version
    2. Checks package dependencies
    3. Creates required directories
    4. Sets up configuration file
    
    Provides feedback for each step and instructions
    for running the application after setup.
    """
    print("Setting up Bug Hunter environment...")
    
    print("\nChecking Python version...")
    check_python_version()
    
    print("\nChecking dependencies...")
    check_dependencies()
    
    print("\nCreating required directories...")
    create_directories()
    
    print("\nSetting up configuration...")
    create_config()
    
    print("\nSetup complete! You can now run the application with:")
    print("python main.py")

if __name__ == '__main__':
    main()
