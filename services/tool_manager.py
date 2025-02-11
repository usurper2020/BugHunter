import os
import git
import json
import requests
from typing import Dict, Any

class ToolManager:
    """Manages external security tools"""
    
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.tools_dir = config.get('TOOLS_DIRECTORY', 'tools')
        os.makedirs(self.tools_dir, exist_ok=True)
        
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
                params=params
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
                
            # Verify main file exists
            main_file_path = os.path.join(tool_path, main_file)
            if not os.path.exists(main_file_path):
                raise FileNotFoundError(f"Main file {main_file} not found")
                
            # Save tool info
            tool_info = {
                "repo_url": repo_url,
                "main_file": main_file,
                "type": self._detect_tool_type(main_file)
            }
            
            with open(os.path.join(tool_path, 'tool_info.json'), 'w') as f:
                json.dump(tool_info, f)
                
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
        """Remove an installed tool"""
        try:
            tool_path = os.path.join(self.tools_dir, tool_name)
            if not os.path.exists(tool_path):
                raise FileNotFoundError(f"Tool {tool_name} not found")
                
            # Remove tool directory
            import shutil
            shutil.rmtree(tool_path)
            
            return {
                "status": "success",
                "message": f"Tool {tool_name} removed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def list_tools(self) -> Dict[str, Any]:
        """List all installed tools"""
        try:
            tools = {}
            for tool_name in os.listdir(self.tools_dir):
                tool_path = os.path.join(self.tools_dir, tool_name)
                info_path = os.path.join(tool_path, 'tool_info.json')
                
                if os.path.isdir(tool_path) and os.path.exists(info_path):
                    with open(info_path, 'r') as f:
                        tools[tool_name] = json.load(f)
                        
            return {
                "status": "success",
                "tools": tools
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _detect_tool_type(self, main_file: str) -> str:
        """Detect tool type based on main file extension"""
        ext = os.path.splitext(main_file)[1].lower()
        return {
            '.py': 'Python',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.js': 'JavaScript',
            '.rs': 'Rust'
        }.get(ext, 'Unknown')
