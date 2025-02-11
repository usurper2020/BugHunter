class ContributionSystem:
    def __init__(self):
        self.initialized = False
        self.contributions = []
        
    def initialize(self):
        """Initialize contribution system"""
        self.initialized = True
        
    def log_contribution(self, contribution_data):
        """Log a contribution"""
        if not self.initialized:
            raise RuntimeError("Contribution system not initialized")
            
        contribution_record = {
            'data': contribution_data,
            'logged': True,
            'timestamp': None  # Could add actual timestamp if needed
        }
        
        self.contributions.append(contribution_record)
        return contribution_record
        
    def get_contributions(self):
        """Get all logged contributions"""
        return self.contributions
        
    def get_status(self):
        """Get the current status of contribution system"""
        return {
            'initialized': self.initialized,
            'contribution_count': len(self.contributions),
            'status': 'running' if self.initialized else 'not initialized'
        }
