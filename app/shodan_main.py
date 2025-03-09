import json
import logging
from typing import Dict, List
import os
from tool_manager import ToolManager
from shodan_integration import ShodanIntegration
from scanning_profiles import ScanningProfiles
from config_manager import ConfigManager  # Import ConfigManager
import sys
from dotenv import load_dotenv
from shodan import Shodan

class ScanningProfiles:
    """Manages scanning profiles for the BugHunter application.
    This class provides functionality to:
    - Load and save scanning profiles from/to JSON file
    - Add new scanning profiles
    - Retrieve existing profiles
    - Manage profile parameters and configurations
    Profiles are stored in a JSON file for persistence between
    application sessions.
    """
    def __init__(self, config_manager, filename):
        """
        Initialize the ScanningProfiles manager.
        Parameters:
        config_manager: Configuration manager instance
        filename (str): Path to the JSON file storing profiles.
        """
        self.config_manager = config_manager
        self.filename = filename

    def load_profiles(self):
        """
        Load scanning profiles from the JSON file.
        Returns:
        dict: Dictionary of profile configurations.
        Returns empty dict if file not found.
        Note:
        Silently handles file not found errors by returning
        an empty dictionary, allowing for first-time use.
        """
        print(f"Loading scanning profiles from {self.filename}")
        if not os.path.exists(self.filename):
            print(f"File {self.filename} not found. Returning empty profiles.")
            return {}
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                profiles = json.load(f)  # Load the JSON content
                return profiles
        except Exception as e:
            print(f"Failed to load profiles: {e}")
            return {}

class BugHunterApp:
    def __init__(self):
        try:
            print("Initializing BugHunterApp...")
            load_dotenv()  # Load environment variables from .env file
            SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
            print(f"Loaded SHODAN_API_KEY: {SHODAN_API_KEY}")
            if not SHODAN_API_KEY:
                raise ValueError("Shodan API key not found in environment variables.")
            self.tool_manager = ToolManager(SHODAN_API_KEY)
            print("BugHunterApp initialized.")
        except Exception as e:
            print(f"Error initializing BugHunterApp: {e}")
            sys.exit(1)
        try:
            self.shodan_api = self.initialize_shodan()
        except Exception as e:
            logging.error(f"Failed to initialize Shodan: {e}")
            self.shodan_api = None  # Ensure the application continues to start

    def initialize_shodan(self):
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            raise ValueError("Shodan API key is missing")
        return Shodan(api_key)

    def run(self):
        try:
            print("Running BugHunterApp...")
            # Add your application logic here
            self.tool_manager.use_profile("Default Scan")
            self.tool_manager.use_profile("Advanced Scan")
            print("BugHunterApp run completed.")
        except Exception as e:
            print(f"Error running BugHunterApp: {e}")

def main():
    try:
        print("Starting main function...")
        app = BugHunterApp()
        app.run()
        print("Main function completed.")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        sys.exit(1)