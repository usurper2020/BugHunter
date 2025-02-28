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
        self.config_manager = config_manager
        self.scopes = {}
        self.logger.debug("ScopeManager initialized")
        self._initialize_default_scope()


    
    def create_scope(self, scope_name: str, targets: List[str]) -> bool:
        """
        Create a new scanning scope
        
        Args:
            scope_name: Name of the scope
            targets: List of targets to include in the scope
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.debug(f"Attempting to create scope '{scope_name}' with {len(targets)} targets")
        try:
            if scope_name in self.scopes:
                raise ValueError(f"Scope '{scope_name}' already exists")
                
            self.scopes[scope_name] = {
                'targets': targets,
                'created_at': datetime.now()
            }
            self.logger.info(f"Created scope '{scope_name}' with {len(targets)} targets")
            self.logger.debug(f"Scope '{scope_name}' details: {self.scopes[scope_name]}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create scope: {str(e)}", exc_info=True)
            return False

            
    def get_scope(self, scope_name: str) -> Optional[Dict[str, any]]:
        """
        Get scope details
        
        Args:
            scope_name: Name of the scope to retrieve
            
        Returns:
            Scope dictionary if found, None otherwise
        """
        try:
            return self.scopes.get(scope_name)
        except Exception as e:
            self.logger.error(f"Failed to get scope: {str(e)}")
            return None
            
    def update_scope(self, scope_name: str, targets: List[str]) -> bool:
        """
        Update an existing scope
        
        Args:
            scope_name: Name of the scope to update
            targets: New list of targets for the scope
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if scope_name not in self.scopes:
                raise ValueError(f"Scope '{scope_name}' does not exist")
                
            self.scopes[scope_name]['targets'] = targets
            self.logger.info(f"Updated scope '{scope_name}' with {len(targets)} targets")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update scope: {str(e)}")
            return False
            
    def delete_scope(self, scope_name: str) -> bool:
        """
        Delete a scope
        
        Args:
            scope_name: Name of the scope to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if scope_name not in self.scopes:
                raise ValueError(f"Scope '{scope_name}' does not exist")
                
            del self.scopes[scope_name]
            self.logger.info(f"Deleted scope '{scope_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete scope: {str(e)}")
            return False
            
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

    def add_target(self, target: str, scope_name: str = 'default_scope') -> bool:
        """
        Add a target to a specific scope
        
        Args:
            target: The target to add (e.g., domain or IP)
            scope_name: Name of the scope to add the target to
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.debug(f"Attempting to add target '{target}' to scope '{scope_name}'")
        try:
            if not self.scope_exists(scope_name):
                self.logger.warning(f"Scope '{scope_name}' does not exist")
                return False
            
            if target in self.scopes[scope_name]['targets']:
                self.logger.warning(f"Target '{target}' already exists in scope '{scope_name}'")
                return False
                
            self.scopes[scope_name]['targets'].append(target)
            self.logger.info(f"Added target '{target}' to scope '{scope_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add target: {str(e)}", exc_info=True)
            return False

    def remove_target(self, target: str, scope_name: str = 'default_scope') -> bool:
        """
        Remove a target from a specific scope
        
        Args:
            target: The target to remove (e.g., domain or IP)
            scope_name: Name of the scope to remove the target from
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.debug(f"Attempting to remove target '{target}' from scope '{scope_name}'")
        try:
            if not self.scope_exists(scope_name):
                self.logger.warning(f"Scope '{scope_name}' does not exist")
                return False
            
            if target not in self.scopes[scope_name]['targets']:
                self.logger.warning(f"Target '{target}' not found in scope '{scope_name}'")
                return False
                
            self.scopes[scope_name]['targets'].remove(target)
            self.logger.info(f"Removed target '{target}' from scope '{scope_name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove target: {str(e)}", exc_info=True)
            return False

    def get_targets(self, scope_name: str) -> Optional[List[str]]:

        """
        Get targets for a specific scope
        
        Args:
            scope_name: Name of the scope to retrieve targets for
            
        Returns:
            List of targets if scope exists, empty list if scope doesn't exist
        """
        self.logger.debug(f"Retrieving targets for scope '{scope_name}'")
        try:
            if not self.scope_exists(scope_name):
                self.logger.warning(f"Scope '{scope_name}' does not exist")
                return []
            targets = self.scopes[scope_name]['targets']
            self.logger.debug(f"Found {len(targets)} targets in scope '{scope_name}'")
            return targets
        except Exception as e:
            self.logger.error(f"Failed to get targets: {str(e)}", exc_info=True)
            return []



    def export_scope(self, scope_name: str, output_path: Path) -> bool:

        """
        Export a scope to a file
        
        Args:
            scope_name: Name of the scope to export
            output_path: Path to save the exported scope
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if scope_name not in self.scopes:
                raise ValueError(f"Scope '{scope_name}' does not exist")
                
            with open(output_path, 'w') as f:
                json.dump(self.scopes[scope_name], f)
            self.logger.info(f"Exported scope '{scope_name}' to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export scope: {str(e)}")
            return False
