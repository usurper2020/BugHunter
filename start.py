#!/usr/bin/env python3
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import and run the main application
from src.main_app import main

if __name__ == '__main__':
    try:
        # Ensure we're in the project root directory
        os.chdir(project_root)
        
        # Run the application
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)
