# services/tool_manager.py

import os
import git
import json
import requests
from typing import Dict, Any, List

class ToolManager:
    def __init__(self):  # Remove any parameters here
        """Initialize the tool manager"""
        try:
            # Load configuration
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            # Set up directories
            self.tools_dir = config.get('TOOLS_DIRECTORY', 'tools')
            self.converted_dir = os.path.join(self.tools_dir, 'converted')
            
            # Create directories if they don't exist
            os.makedirs(self.tools_dir, exist_ok=True)
            os.makedirs(self.converted_dir, exist_ok=True)
            
            # Initialize tool storage
            self.installed_tools = {}
            self.load_installed_tools()
            
        except Exception as e:
            print(f"Error initializing ToolManager: {e}")
            # Set default values
            self.tools_dir = 'tools'
            self.converted_dir = os.path.join(self.tools_dir, 'converted')
            self.installed_tools = {}

    def load_installed_tools(self):
        """Load information about installed tools"""
        try:
            tools_info_path = os.path.join(self.tools_dir, 'tools_info.json')
            if os.path.exists(tools_info_path):
                with open(tools_info_path, 'r') as f:
                    self.installed_tools = json.load(f)
        except Exception as e:
            print(f"Error loading installed tools: {e}")
            self.installed_tools = {}

    def search_github_tools(self, query: str, language: str = None) -> Dict[str, Any]:
        """Search for security tools on GitHub"""
        try:
            params = {
                'q': f'{query} in:name,description topic:security',
                'sort': 'stars',
                'order': 'desc'
            }
            
            if language:
                params['q'] += f' language:{language}'
                
            response = requests.get(
                'https://api.github.com/search/repositories',
                params=params,
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            response.raise_for_status()
            
            return {
                "status": "success",
                "results": response.json()['items']
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def install_github_tool(self, repo_url: str, main_file: str) -> Dict[str, Any]:
        """Install a tool from GitHub"""
        try:
            repo_name = repo_url.split('/')[-1]
            tool_path = os.path.join(self.tools_dir, repo_name)
            
            # Clone or update repository
            if os.path.exists(tool_path):
                repo = git.Repo(tool_path)
                repo.remotes.origin.pull()
            else:
                git.Repo.clone_from(repo_url, tool_path)
                
            # Save tool info
            self.installed_tools[repo_name] = {
                "repo_url": repo_url,
                "main_file": main_file,
                "status": "installed",
                "version": "latest"
            }
            
            self._save_tools_info()
            
            return {
                "status": "success",
                "message": f"Tool {repo_name} installed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def uninstall_tool(self, tool_name: str) -> Dict[str, Any]:
        """Uninstall a tool"""
        try:
            tool_path = os.path.join(self.tools_dir, tool_name)
            
            if os.path.exists(tool_path):
                shutil.rmtree(tool_path)
                
            if tool_name in self.installed_tools:
                del self.installed_tools[tool_name]
                self._save_tools_info()
                
            return {
                "status": "success",
                "message": f"Tool {tool_name} uninstalled successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def list_tools(self) -> Dict[str, Any]:
        """Get list of installed tools"""
        try:
            return {
                "status": "success",
                "tools": self.installed_tools
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _save_tools_info(self):
        """Save tools information to file"""
        try:
            tools_info_path = os.path.join(self.tools_dir, 'tools_info.json')
            with open(tools_info_path, 'w') as f:
                json.dump(self.installed_tools, f, indent=4)
        except Exception as e:
            print(f"Error saving tools info: {e}")
