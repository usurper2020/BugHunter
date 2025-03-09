# filepath: c:\Users\clabb\Desktop\BugHunter\main.py
import os
import sys
from dotenv import load_dotenv
from tool_manager import ToolManager

class BugHunterApp:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
        if not SHODAN_API_KEY:
            raise ValueError("Shodan API key not found in environment variables.")
        self.tool_manager = ToolManager(SHODAN_API_KEY)

    def run(self):
        # Add your application logic here
        self.tool_manager.use_profile("Default Scan")
        self.tool_manager.use_profile("Advanced Scan")

def main():
    app = BugHunterApp()
    app.run()

if __name__ == "__main__":
    sys.exit(main())