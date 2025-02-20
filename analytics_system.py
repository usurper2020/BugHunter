class AnalyticsSystem:
    """
    Class for managing analytics monitoring within the BugHunter application.
    
    This class handles the monitoring of system analytics and provides
    status information about the monitoring system.
    """
    
    def __init__(self):
        """
        Initialize the AnalyticsSystem instance.
        
        Sets the monitoring state to False, indicating that the analytics
        monitoring system starts in a stopped state.
        """
        self.monitoring = False
        
    def start_monitoring(self):
        """
        Start the analytics monitoring system.
        
        Activates the monitoring system to begin collecting analytics
        data about system usage and performance.
        """
        self.monitoring = True
        
    def get_status(self):
        """
        Retrieve the current status of the analytics monitoring system.
        
        Returns:
            dict: A dictionary containing the monitoring state and the
            current operational status ('running' or 'stopped').
        """
        return {
            'monitoring': self.monitoring,
            'status': 'running' if self.monitoring else 'stopped'
        }
