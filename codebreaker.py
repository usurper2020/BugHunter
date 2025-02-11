class CodeBreaker:
    def __init__(self):
        self.initialized = False
        
    def initialize(self):
        """Initialize the CodeBreaker system"""
        self.initialized = True
        
    def get_status(self):
        """Get the current status of the CodeBreaker system"""
        return {
            'initialized': self.initialized,
            'status': 'running' if self.initialized else 'not initialized'
        }
