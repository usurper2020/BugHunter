import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from collaboration_dialog import CollaborationDialog
from collaboration import Collaboration
from contribution_dialog import ContributionDialog
from contribution_system import ContributionSystem
from notification import NotificationSystem

class CollaborationSystem:
    def __init__(self, config=None):
        self.config = config or {}
        self.collaboration = Collaboration()
        self.collaboration_dialog = CollaborationDialog()
        self.contribution_dialog = ContributionDialog()
        self.contribution_system = ContributionSystem()
        self.notification = NotificationSystem()
        
    def initialize(self):
        """Initialize all collaboration subsystems"""
        # Setup notification system
        self.notification.initialize()
        
        # Initialize collaboration features
        self.collaboration.initialize()
        
        # Setup contribution system
        self.contribution_system.initialize()
        
    def share_report(self, report_data):
        """Share a report with collaborators"""
        # Process the report
        processed_report = self.collaboration.process_report(report_data)
        
        # Send notifications
        self.notification.notify_collaborators(processed_report)
        
        # Log contribution
        self.contribution_system.log_contribution(processed_report)
        
        return processed_report
        
    def get_collaboration_status(self):
        """Get status of all collaboration subsystems"""
        return {
            'collaboration_status': self.collaboration.get_status(),
            'contribution_status': self.contribution_system.get_status(),
            'notification_status': self.notification.get_status()
        }
        
    def show_collaboration_dialog(self):
        """Show the collaboration dialog"""
        return self.collaboration_dialog.show()
        
    def show_contribution_dialog(self):
        """Show the contribution dialog"""
        return self.contribution_dialog.show()
