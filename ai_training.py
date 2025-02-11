class AITraining:
    def __init__(self):
        self.initialized = False
        self.training_data = []
        
    def initialize(self):
        """Initialize training system"""
        self.initialized = True
        
    def train_on_interaction(self, message, response):
        """Train on a message-response pair"""
        if not self.initialized:
            raise RuntimeError("Training system not initialized")
        self.training_data.append({
            'message': message,
            'response': response,
            'timestamp': None  # Could add actual timestamp if needed
        })
        
    def get_training_data(self):
        """Get collected training data"""
        return self.training_data
        
    def clear_training_data(self):
        """Clear training data"""
        self.training_data = []
        
    def get_status(self):
        """Get the current status of training system"""
        return {
            'initialized': self.initialized,
            'training_samples': len(self.training_data),
            'status': 'running' if self.initialized else 'not initialized'
        }
