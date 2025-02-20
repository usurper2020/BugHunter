class Middleware:
    """
    Middleware system for managing application configuration and state.
    
    This class provides a centralized system for:
    - Managing application configuration
    - Tracking initialization state
    - Providing status information
    
    The middleware acts as an intermediary layer between
    different components of the application, facilitating
    configuration management and state tracking.
    """
    
    def __init__(self):
        """
        Initialize the Middleware instance.
        
        Sets up:
        - Initialization state (initially False)
        - Empty configuration dictionary
        """
        self.initialized = False
        self.config = {}
        
    def setup(self):
        """
        Set up and initialize the middleware system.
        
        Prepares the middleware for use by setting the
        initialization flag to True. This method should
        be called before using other middleware features.
        """
        self.initialized = True
        
    def get_status(self):
        """
        Retrieve the current status of the middleware system.
        
        Returns:
            dict: A status dictionary containing:
                - initialized: Boolean indicating if system is initialized
                - status: String status ('running' or 'not initialized')
        """
        return {
            'initialized': self.initialized,
            'status': 'running' if self.initialized else 'not initialized'
        }
        
    def add_config(self, key, value):
        """
        Add or update a configuration value.
        
        Parameters:
            key: Configuration key to set
            value: Value to associate with the key
            
        The configuration is stored in memory and remains
        available until the application terminates.
        """
        self.config[key] = value
        
    def get_config(self, key, default=None):
        """
        Retrieve a configuration value.
        
        Parameters:
            key: Configuration key to retrieve
            default: Value to return if key doesn't exist
            
        Returns:
            The value associated with the key, or the default
            value if the key is not found.
        """
        return self.config.get(key, default)
