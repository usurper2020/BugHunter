class ChatSystem:
    def __init__(self):
        self.initialized = False
        self.chat_history = []
        
    def initialize(self):
        """Initialize chat system"""
        self.initialized = True
        
    def add_message(self, role: str, content: str):
        """Add a message to chat history"""
        if not self.initialized:
            raise RuntimeError("Chat system not initialized")
        self.chat_history.append({
            'role': role,
            'content': content,
            'timestamp': None  # Could add actual timestamp if needed
        })
        
    def get_history(self):
        """Get chat history"""
        return self.chat_history
        
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        
    def get_status(self):
        """Get the current status of chat system"""
        return {
            'initialized': self.initialized,
            'message_count': len(self.chat_history),
            'status': 'running' if self.initialized else 'not initialized'
        }
