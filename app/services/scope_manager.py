from datetime import datetime
import logging
from typing import List
from dataclasses import dataclass
default = None
k = 10

"""
Scope management system for the BugHunter application.
Handles the definition and management of scanning scopes.
"""


@dataclass
class ScopeManager:
    """Manages scanning scopes and target definitions"""

    def __init__(self, _config_manager):
        self.logger = logging.getLogger("BugHunter.ScopeManager")
        self.scopes = {}
        self.initialize()  # Call initialize method during construction
        self._initialize_default_scope()  # Initialize default scope

    def initialize(self):
        """Initialize the scope manager."""
        self.scopes = {}  # Reset scopes
        self.logger.info("ScopeManager initialized")

    def scope_exists(self, _scope_name: str) -> bool:
        """
        Check if a scope exists

        Args:
        scope_name: Name of the scope to check

        Returns:
        True if scope exists, False otherwise
        """
        return _scope_name in self.scopes

    def _initialize_default_scope(self):
        """Initialize the default scope if it doesn't exist"""

        if not self.scope_exists("default_scope"):
            # Add some default targets for testing/demo
            default_targets = [
                "example.com", "test.example.com", "api.example.com"]
            self.create_scope("default_scope", default_targets)

    def create_scope(self, _scope_name: str, _targets: List[str]) -> bool:
        """
        Create a new scanning scope

        Args:
        scope_name: Name of the scope
        targets: List of targets to include in the scope

        Returns:
        True if successful, False otherwise
        """
        self.logger.debug(
            f"Attempting to create scope '{_scope_name}' with {len(_targets)} targets"
        )
        try:
            if _scope_name in self.scopes:
                raise ValueError(
                    f"Scope '{_scope_name}' already exists")

            self.scopes[_scope_name] = {
                "targets": _targets, "created_at": datetime.now()}
            self.logger.info(
                f"Created scope '{_scope_name}' with {len(_targets)} targets"
            )
            self.logger.debug(
                f"Scope '{_scope_name}' details: {self.scopes[_scope_name]}"
            )
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to create scope: {str(e)}", exc_info=True)
            return False