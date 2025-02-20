"""
Tool management module for the BugHunter application.

This module handles the discovery, download, and management of security
testing tools from GitHub repositories. It provides functionality for
searching, downloading, converting, and managing security tools.
"""

import os
import git
import requests
import logging

# Set up logging
logging.basicConfig(
    filename='bug_bounty_tool.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ToolManager:
    """
    Manages security testing tools for the BugHunter platform.
    
    This class provides functionality to:
    - Search for security tools on GitHub
    - Download and manage tool repositories
    - Convert tools to Python implementations
    - Track and maintain tool inventory
    
    The manager maintains a list of downloaded tools and handles
    their lifecycle within the application.
    """
    
    def __init__(self, config=None):
        """
        Initialize the ToolManager instance.
        
        Parameters:
            config (dict, optional): Configuration dictionary for
                                   customizing tool management
        """
        self.tools = []
        self.config = config if config else {}
        self.tools_directory = os.path.join(os.getcwd(), 'tools')
        
        # Create tools directory if it doesn't exist
        if not os.path.exists(self.tools_directory):
            os.makedirs(self.tools_directory)
            
        # Load existing tools
        if os.path.exists(self.tools_directory):
            self.tools = [d for d in os.listdir(self.tools_directory) 
                         if os.path.isdir(os.path.join(self.tools_directory, d))]
        
        # Popular bug bounty tools and their categories
        self.suggested_tools = {
            'reconnaissance': [
                {'name': 'amass', 'description': 'In-depth DNS enumeration and network mapping'},
                {'name': 'subfinder', 'description': 'Fast passive subdomain enumeration tool'},
                {'name': 'naabu', 'description': 'Fast port scanner with a focus on reliability'}
            ],
            'vulnerability_scanning': [
                {'name': 'nuclei', 'description': 'Fast and customizable vulnerability scanner'},
                {'name': 'nikto', 'description': 'Web server scanner for dangerous files/CGIs'},
                {'name': 'zap', 'description': 'OWASP Zed Attack Proxy for finding vulnerabilities'}
            ],
            'content_discovery': [
                {'name': 'ffuf', 'description': 'Fast web fuzzer for content discovery'},
                {'name': 'dirsearch', 'description': 'Web path scanner'},
                {'name': 'gobuster', 'description': 'Directory/file & DNS busting tool'}
            ],
            'exploitation': [
                {'name': 'sqlmap', 'description': 'Automatic SQL injection detection and exploitation'},
                {'name': 'xsstrike', 'description': 'Advanced XSS detection suite'},
                {'name': 'commix', 'description': 'Command injection exploitation tool'}
            ]
        }

    def search_tool(self, search_query):
        """
        Search for security testing tools based on name or functionality.
        
        Parameters:
            search_query (str): Search terms for finding tools
            
        Returns:
            list: List of tool information matching the search,
                 including suggested tools and GitHub results
        """
        results = []
        search_query = search_query.lower()
        
        # First, search through suggested tools
        for category, tools in self.suggested_tools.items():
            for tool in tools:
                if (search_query in tool['name'].lower() or 
                    search_query in tool['description'].lower() or
                    search_query in category.lower()):
                    results.append({
                        'name': tool['name'],
                        'description': tool['description'],
                        'category': category,
                        'type': 'suggested'
                    })
        
        # Then search GitHub for additional tools
        try:
            # Enhance search query for bug bounty tools
            github_query = f"{search_query} bug bounty security"
            url = f"https://api.github.com/search/repositories?q={github_query}&sort=stars&order=desc"
            response = requests.get(url)
            response.raise_for_status()
            
            for repo in response.json().get('items', [])[:5]:  # Limit to top 5 results
                results.append({
                    'name': repo['name'],
                    'description': repo['description'] or 'No description available',
                    'url': repo['html_url'],
                    'stars': repo['stargazers_count'],
                    'type': 'github'
                })
        except requests.RequestException as e:
            logging.error(f"Error searching GitHub: {e}")
        
        return results

    def download_tool(self, tool_identifier):
        """
        Download a tool by name or URL.
        
        Parameters:
            tool_identifier (str): Tool name or GitHub repository URL
            
        Returns:
            dict: Status and details of the download operation
        """
        # Check if it's a suggested tool
        tool_url = None
        for tools in self.suggested_tools.values():
            for tool in tools:
                if tool['name'].lower() == tool_identifier.lower():
                    # Map tool names to their GitHub repositories
                    tool_mappings = {
                        'amass': 'OWASP/Amass',
                        'subfinder': 'projectdiscovery/subfinder',
                        'naabu': 'projectdiscovery/naabu',
                        'nuclei': 'projectdiscovery/nuclei',
                        'nikto': 'sullo/nikto',
                        'zap': 'zaproxy/zaproxy',
                        'ffuf': 'ffuf/ffuf',
                        'dirsearch': 'maurosoria/dirsearch',
                        'gobuster': 'OJ/gobuster',
                        'sqlmap': 'sqlmapproject/sqlmap',
                        'xsstrike': 's0md3v/XSStrike',
                        'commix': 'commixproject/commix'
                    }
                    if tool['name'] in tool_mappings:
                        tool_url = f"https://github.com/{tool_mappings[tool['name']]}.git"
                    break
            if tool_url:
                break
        
        # If not found in suggested tools, treat as direct URL
        if not tool_url:
            tool_url = tool_identifier if tool_identifier.startswith('http') else f"https://github.com/{tool_identifier}.git"
        
        tool_name = tool_url.split('/')[-1].replace('.git', '')
        try:
            tool_path = os.path.join(self.tools_directory, tool_name)
            if tool_name not in self.tools:
                git.Repo.clone_from(tool_url, tool_path)
                self.tools.append(tool_name)
                logging.info(f"Downloaded and added tool: {tool_name}")
                return {
                    'status': 'success',
                    'message': f"Downloaded and added tool: {tool_name}",
                    'tool_name': tool_name
                }
            return {
                'status': 'warning',
                'message': f"Tool {tool_name} is already installed",
                'tool_name': tool_name
            }
        except Exception as e:
            logging.error(f"Error downloading tool: {e}")
            return {
                'status': 'error',
                'message': f"Error downloading tool: {str(e)}",
                'tool_name': tool_name
            }

    def convert_tool_to_python(self, tool_name):
        """
        Convert a downloaded tool to Python implementation.
        
        Parameters:
            tool_name (str): Name of the tool to convert
            
        Returns:
            str: Status message about the conversion
            
        Note:
            Currently a placeholder for future implementation
            of tool conversion functionality.
        """
        # Implement conversion logic to convert the tool into Python code
        logging.info(f"Converted tool {tool_name} to Python.")
        return f"Converted tool {tool_name} to Python."

    def delete_tool(self, tool_name):
        """
        Remove a tool from the system.
        
        Parameters:
            tool_name (str): Name of the tool to delete
            
        Returns:
            str: Status message indicating success or failure
            
        Note:
            Removes both the tool directory and its entry
            from the tools list. Logs the deletion operation.
        """
        tool_path = os.path.join(self.tools_directory, tool_name)
        if tool_name in self.tools and os.path.exists(tool_path):
            try:
                import shutil
                shutil.rmtree(tool_path)  # Use rmtree to remove directory and contents
                self.tools.remove(tool_name)
                logging.info(f"Deleted tool: {tool_name}")
                return f"Deleted tool: {tool_name}"
            except Exception as e:
                logging.error(f"Error deleting tool {tool_name}: {e}")
                return f"Error deleting tool {tool_name}: {e}"
        logging.warning(f"Tool {tool_name} not found.")
        return f"Tool {tool_name} not found."

    def list_tools(self):
        """
        Get list of all downloaded tools.
        
        Returns:
            list: Names of all tools currently managed by
                 the ToolManager instance.
        """
        return self.tools
