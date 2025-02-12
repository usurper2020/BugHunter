"""
Scan target model for the BugHunter application.

This module provides a class for representing scan targets
with proper JSON serialization support.
"""

class ScanTarget:
    """
    Class representing a scan target.
    
    This class provides:
    - Target URL and metadata storage
    - JSON serialization support
    - String representation
    """
    
    def __init__(self, url, scope=None, metadata=None):
        """
        Initialize a scan target.
        
        Parameters:
            url (str): Target URL to scan
            scope (str, optional): Scope identifier
            metadata (dict, optional): Additional target metadata
        """
        self.url = url
        self.scope = scope
        self.metadata = metadata or {}
        
    def to_dict(self):
        """
        Convert the scan target to a dictionary.
        
        Returns:
            dict: Dictionary representation of the scan target
        """
        return {
            'url': self.url,
            'scope': self.scope,
            'metadata': self.metadata
        }
        
    def __str__(self):
        """String representation of the scan target."""
        return f"ScanTarget(url='{self.url}', scope='{self.scope}')"
