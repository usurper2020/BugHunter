"""
Scope management system for the BugHunter application.
Handles the definition and management of scanning scopes.
"""

import logging
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class ScopeManager:
    """Manages scanning scopes and target definitions"""

    def __init__(self, config_manager):
        self.logger = logging.getLogger('BugHunter.ScopeManager')
        self.scopes = {}
        self.initialize()  # Call initialize method during construction
        self._initialize_default_scope()  # Initialize default scope

    def initialize(self):
        """Initialize the scope manager."""
        self.scopes = {}  # Reset scopes
        self.logger.info("ScopeManager initialized")

    def scope_exists(self, scope_name: str) -> bool:
        """
        Check if a scope exists

        Args:
            scope_name: Name of the scope to check

        Returns:
            True if scope exists, False otherwise
        """
        return scope_name in self.scopes

    def _initialize_default_scope(self):
        """Initialize the default scope if it doesn't exist"""

        """
        Initialize the default scope if it doesn't exist
        """
        if not self.scope_exists('default_scope'):
            # Add some default targets for testing/demo
            default_targets = [
                'example.com',
                'test.example.com',
                'api.example.com'
            ]
            self.create_scope('default_scope', default_targets)

    def create_scope(self, scope_name: str, targets: List[str]) -> bool:
        """
        Create a new scanning scope

        Args:
            scope_name: Name of the scope
            targets: List of targets to include in the scope

        Returns:
            True if successful, False otherwise
        """
        self.logger.debug(
            f"Attempting to create scope '{scope_name}' with {len(targets)} targets")
        try:
            if scope_name in self.scopes:
                raise ValueError(f"Scope '{scope_name}' already exists")

            self.scopes[scope_name] = {
                'targets': targets,
                'created_at': datetime.now()
            }
            self.logger.info(
                f"Created scope '{scope_name}' with {len(targets)} targets")
            self.logger.debug(
                f"Scope '{scope_name}' details: {self.scopes[scope_name]}")
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to create scope: {str(e)}", exc_info=True)
            return False
