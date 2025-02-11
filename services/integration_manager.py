import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from shodan_integration import ShodanIntegration
from wayback_machine_integration import WaybackMachineIntegration

class IntegrationManager:
    def __init__(self, config=None):
        self.config = config or {}
        self.shodan = ShodanIntegration()
        self.wayback = WaybackMachineIntegration()
        self.initialized = False
        
    def initialize_integrations(self):
        """Initialize all external service integrations"""
        self.initialized = True
        
    def get_integration_status(self):
        """Get status of all integrations"""
        return {
            'initialized': self.initialized,
            'status': 'running' if self.initialized else 'not initialized',
            'shodan': self.shodan.get_status() if hasattr(self.shodan, 'get_status') else 'unknown',
            'wayback': self.wayback.get_status() if hasattr(self.wayback, 'get_status') else 'unknown'
        }
        
    def perform_integrated_scan(self, target):
        """Perform a scan using all available integrations"""
        if not self.initialized:
            raise RuntimeError("Integration manager not initialized")
            
        results = {
            'target': target,
            'shodan_results': self.shodan.search(target) if hasattr(self.shodan, 'search') else None,
            'wayback_results': self.wayback.get_snapshots(target) if hasattr(self.wayback, 'get_snapshots') else None
        }
        return results
