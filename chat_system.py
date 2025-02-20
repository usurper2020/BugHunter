class ChatSystem:
    """
    Class for managing chat interactions within the BugHunter application.
    
    This class handles message sending and receiving between the user
    and the AI system, while maintaining a history of conversations.
    """
    
    def __init__(self):
        """
        Initialize the ChatSystem instance.
        
        Creates an empty list to store the chat history of messages
        exchanged between the user and the AI.
        """
        self.history = []

    def send_message(self, message):
        """
        Send a message to the AI system.
        
        This method processes the user's message and generates an AI response.
        The message is added to the chat history before processing.
        
        Parameters:
            message (str): The message to be sent to the AI.
            
        Returns:
            str: The AI's response to the message.
        """
        self.history.append(message)
        # Simulate AI response
        return "AI Response to: " + message

    def receive_message(self):
        """
        Retrieve the most recent message from the chat history.
        
        Returns:
            str: The most recent message in the chat history, or
            'No messages yet.' if the history is empty.
        """
        return self.history[-1] if self.history else "No messages yet."
