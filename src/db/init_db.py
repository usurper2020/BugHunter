#!/usr/bin/env python3
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

def init_database(config):
    """Initialize the database using the provided configuration"""
    try:
        print("Starting database initialization...")
        
        # First try to connect to PostgreSQL server
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("Connected to PostgreSQL server successfully")
        
        # Read SQL schema
        schema_path = Path(__file__).parent / 'schema.sql'
        print(f"Reading schema from {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_schema = f.read()
        
        # Split schema into individual statements
        statements = sql_schema.split(';')
        
        # Execute each statement
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                try:
                    print(f"\nExecuting statement:\n{statement[:100]}...")  # Show first 100 chars
                    cur.execute(statement)
                    print("Statement executed successfully")
                except psycopg2.Error as e:
                    print(f"Error executing statement: {str(e)}")
                    # Continue with other statements even if one fails
                    continue
        
        # Close database connection
        cur.close()
        conn.close()
        
        print("\nDatabase initialization completed successfully!")
        print("\nDefault admin credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("\nIMPORTANT: Please change these credentials immediately after first login.")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\nDatabase error: {str(e)}")
        if 'password authentication failed' in str(e).lower():
            print("\nTIP: Make sure your PostgreSQL password is correctly set in config.json")
        elif 'connection refused' in str(e).lower():
            print("\nTIP: Make sure PostgreSQL server is running and accessible")
        return False
        
    except Exception as e:
        print(f"\nError initializing database: {str(e)}")
        return False

def check_postgres_connection(config):
    """Check if PostgreSQL server is accessible"""
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        conn.close()
        return True
    except:
        return False

if __name__ == '__main__':
    # Add project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(project_root)
    
    # Import configuration
    from src.core import config
    
    print("Bug Hunter Database Initialization")
    print("=================================")
    
    # Check PostgreSQL connection first
    if not check_postgres_connection(config.config):
        print("\nERROR: Could not connect to PostgreSQL server!")
        print("Please make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. The database configuration in config.json is correct")
        print("3. The PostgreSQL user has appropriate permissions")
        sys.exit(1)
    
    # Initialize database
    if init_database(config.config):
        print("\nDatabase setup completed successfully!")
    else:
        print("\nDatabase setup failed. Please check the error messages above.")
        sys.exit(1)
