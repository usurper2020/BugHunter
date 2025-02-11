#!/usr/bin/env python3
import os
import json
import secrets
import shutil
from pathlib import Path
import argparse
import subprocess
import sys

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def install_dependencies():
    """Install dependencies with conflict resolution"""
    try:
        # First, upgrade pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        print("Upgraded pip successfully")
        
        # Install dependencies with --no-deps first to avoid conflicts
        print("Installing core dependencies...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            '--no-deps', '-r', 'requirements-new.txt'
        ], check=True)
        
        # Then install dependencies normally, allowing pip to resolve conflicts
        print("Resolving dependencies...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            '-r', 'requirements-new.txt'
        ], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def setup_environment(args):
    """Set up the application environment"""
    print("Setting up Bug Hunter environment...")
    
    # Create necessary directories
    directories = ['logs', 'data', 'reports', 'templates', 'tools', 'cache']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

    # Create config file from template
    if not os.path.exists('config.json') or args.force:
        if os.path.exists('config.template.json'):
            with open('config.template.json', 'r') as f:
                config = json.load(f)
            
            # Generate secure JWT secret key
            config['JWT_SECRET_KEY'] = generate_secret_key()
            print("Generated secure JWT secret key")
            
            # Update with provided CodeGPT API key if available
            if args.api_key:
                config['AI_API_KEY'] = args.api_key
                print("Added CodeGPT API key to configuration")
            
            # Update with provided database settings if available
            if args.db_password:
                config['DB_PASSWORD'] = args.db_password
                print("Added database password to configuration")
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            print("Created config.json with secure defaults")
        else:
            print("Error: config.template.json not found")
            return False

    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv') or args.force:
        try:
            print("Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print("Created virtual environment successfully")

            # Install dependencies
            if not install_dependencies():
                print("Failed to install dependencies")
                return False

            print("\nEnvironment setup completed successfully!")
            
            # Print next steps
            print("\nNext steps:")
            if not args.api_key:
                print("1. Add your CodeGPT API key to config.json")
            if not args.db_password:
                print("2. Update database settings in config.json")
            print("3. Activate virtual environment:")
            if os.name == 'nt':
                print("   venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
            print("4. Run the application:")
            print("   python run.py")
            
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error setting up environment: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Set up Bug Hunter environment')
    parser.add_argument('--api-key', help='CodeGPT API key')
    parser.add_argument('--db-password', help='Database password')
    parser.add_argument('--force', action='store_true', help='Force recreation of existing files')
    
    args = parser.parse_args()
    if not setup_environment(args):
        sys.exit(1)

if __name__ == '__main__':
    main()
