class Middleware:
    def __init__(self):
        self.initialized = False
        self.config = {}
        
    def setup(self):
        """Setup the middleware system"""
        self.initialized = True
        
    def get_status(self):
        """Get the current status of the middleware system"""
        return {
            'initialized': self.initialized,
            'status': 'running' if self.initialized else 'not initialized'
        }
        
    def add_config(self, key, value):
        """Add configuration to middleware"""
        self.config[key] = value
        
    def get_config(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
