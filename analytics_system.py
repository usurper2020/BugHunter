class AnalyticsSystem:
    def __init__(self):
        self.monitoring = False
        
    def start_monitoring(self):
        """Start the analytics monitoring system"""
        self.monitoring = True
        
    def get_status(self):
        """Get the current status of the analytics system"""
        return {
            'monitoring': self.monitoring,
            'status': 'running' if self.monitoring else 'stopped'
        }
