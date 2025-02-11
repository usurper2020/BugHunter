#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
import json

def setup_database(args):
    """Set up the database with proper configuration"""
    try:
        print("\nSetting up Bug Hunter Database")
        print("=============================")
        
        # Load or create configuration
        config_file = 'config.json'
        config_template = 'config.template.json'
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        elif os.path.exists(config_template):
            with open(config_template, 'r') as f:
                config = json.load(f)
        else:
            print("Error: No configuration file found")
            return False
        
        # Update database configuration
        config['database'] = {
            'type': 'postgresql',
            'host': args.host or config.get('database', {}).get('host', 'localhost'),
            'port': args.port or config.get('database', {}).get('port', 5432),
            'name': args.name or config.get('database', {}).get('name', 'bughunter_db'),
            'user': args.user or config.get('database', {}).get('user', 'bughunter_user'),
            'password': args.password or config.get('database', {}).get('password', 'your-secure-password-here'),
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': 3600,
            'ssl_mode': 'prefer'
        }
        
        # Save updated configuration
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        print("\nConfiguration updated successfully")
        
        # Initialize database
        print("\nInitializing database...")
        from src.db.init_db import init_database
        
        if init_database(config):
            print("\nDatabase setup completed successfully!")
            return True
        else:
            print("\nDatabase setup failed")
            return False
            
    except Exception as e:
        print(f"\nError setting up database: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Set up Bug Hunter database')
    
    # Database connection options
    parser.add_argument('--host', help='Database host (default: localhost)')
    parser.add_argument('--port', type=int, help='Database port (default: 5432)')
    parser.add_argument('--name', help='Database name (default: bughunter_db)')
    parser.add_argument('--user', help='Database user (default: bughunter_user)')
    parser.add_argument('--password', help='Database password')
    
    args = parser.parse_args()
    
    # Add project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    if setup_database(args):
        print("\nNext steps:")
        print("1. Make sure PostgreSQL is running")
        print("2. Update config.json with your database credentials if needed")
        print("3. Run the application with: python run_integrated.py")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
