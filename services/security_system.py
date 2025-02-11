import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from analytics_system import AnalyticsSystem
from middleware import Middleware
from codebreaker import CodeBreaker

class SecuritySystem:
    def __init__(self, config=None):
        self.config = config or {}
        self.codebreaker = CodeBreaker()
        self.analytics = AnalyticsSystem()
        self.middleware = Middleware()
        
    def initialize(self):
        """Initialize all security subsystems"""
        # Initialize analytics
        self.analytics.start_monitoring()
        
        # Setup middleware
        self.middleware.setup()
        
        # Initialize codebreaker
        self.codebreaker.initialize()
        
    def get_security_status(self):
        """Get the current security status of the system"""
        return {
            'analytics_status': self.analytics.get_status(),
            'middleware_status': self.middleware.get_status(),
            'codebreaker_status': self.codebreaker.get_status()
        }
