import os
import git
import requests
import logging

# Set up logging
logging.basicConfig(filename='bug_bounty_tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ToolManager:
    def __init__(self, config=None):
        self.tools = []
        self.config = config if config else {}

    def search_tool(self, search_query):
        # Search for GitHub tools based on the search_query
        try:
            url = f"https://api.github.com/search/repositories?q={search_query}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get('items', [])
        except requests.RequestException as e:
            logging.error(f"Error searching for tools: {e}")
            return []

    def download_tool(self, repo_url):
        # Download the tool from the provided GitHub repository URL
        tool_name = repo_url.split('/')[-1].replace('.git', '')
        try:
            if tool_name not in self.tools:
                git.Repo.clone_from(repo_url, tool_name)
                self.tools.append(tool_name)
                logging.info(f"Downloaded and added tool: {tool_name}")
                return f"Downloaded and added tool: {tool_name}"
            logging.warning(f"Tool {tool_name} is already added.")
            return f"Tool {tool_name} is already added."
        except Exception as e:
            logging.error(f"Error downloading tool: {e}")
            return f"Error downloading tool: {e}"

    def convert_tool_to_python(self, tool_name):
        # Implement conversion logic to convert the tool into Python code
        logging.info(f"Converted tool {tool_name} to Python.")
        return f"Converted tool {tool_name} to Python."

    def delete_tool(self, tool_name):
        if tool_name in self.tools:
            os.rmdir(tool_name)
            self.tools.remove(tool_name)
            logging.info(f"Deleted tool: {tool_name}")
            return f"Deleted tool: {tool_name}"
        logging.warning(f"Tool {tool_name} not found.")
        return f"Tool {tool_name} not found."

    def list_tools(self):
        return self.tools
