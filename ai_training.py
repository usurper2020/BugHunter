class AITraining:
    """
    Class for managing AI training within the BugHunter application.
    
    This class handles the collection and management of training data
    from user interactions for improving AI responses.
    """
    
    def __init__(self):
        """
        Initialize the AITraining instance.
        
        Sets the initialized state to False and prepares a list to hold
        training data samples.
        """
        self.initialized = True
        
    def train_on_interaction(self, message, response):
        """
        Add a message-response pair to the training data.
        
        This method collects interaction data for future model training.
        
        Parameters:
            message (str): The user's input message.
            response (str): The system's response to the message.
        
        Raises:
            RuntimeError: If the training system has not been initialized.
        """
        if not self.initialized:
            raise RuntimeError("Training system not initialized")
        self.training_data.append({
            'message': message,
            'response': response,
            'timestamp': None  # Could add actual timestamp if needed
        })
        
    def get_training_data(self):
        """
        Retrieve the collected training data.
        
        Returns:
            list: A list of training samples, each containing a message,
            response, and timestamp.
        """
        return self.training_data
        
    def clear_training_data(self):
        """
        Clear all collected training data.
        
        This method resets the training data list to an empty state,
        effectively removing all collected samples.
        """
        self.training_data = []
        
    def get_status(self):
        """
        Retrieve the current status of the training system.
        
        Returns:
            dict: A dictionary containing the initialization status,
            the number of training samples collected, and the current
            operational status.
        """
        return {
            'initialized': self.initialized,
            'training_samples': len(self.training_data),
            'status': 'running' if self.initialized else 'not initialized'
        }
