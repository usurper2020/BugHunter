"""
GitHub Manager for the BugHunter application.

Handles GitHub API interactions and repository management.
"""

import requests
from typing import Dict, Optional
from pathlib import Path

class GitHubManager:
    """Manages GitHub API interactions and repository operations."""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    def get_repository(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Get repository information from GitHub.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary containing repository information or None if failed
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def download_repository(self, owner: str, repo: str, target_dir: Path) -> bool:
        """
        Download a GitHub repository.

        Args:
            owner: Repository owner
            repo: Repository name
            target_dir: Directory to save the repository

        Returns:
            True if download was successful, False otherwise
        """
        url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(target_dir / f"{repo}.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException:
            return False
