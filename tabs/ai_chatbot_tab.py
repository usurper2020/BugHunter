"""
AI Chatbot interface tab for the BugHunter application.

This module provides a simple chat interface for interacting with
the AI system, specifically focused on vulnerability information
retrieval and security-related queries.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from backend.ai_integration import AIIntegration
from backend.models import AIModel

class AIChatbotTab(QWidget):
    """
    Tab widget providing AI chatbot functionality.
    
    This widget creates a simple chat interface with:
    - Text input area for user messages
    - Send button for message submission
    - Response display area for AI output
    - Integration with backend AI systems
    
    The chatbot specializes in providing vulnerability
    and security-related information.
    """
    
    def __init__(self):
        """
        Initialize the AI chatbot interface.
        
        Sets up:
        - UI components and layout
        - Message handling system
        - AI model integration
        - Response display area
        """
        super().__init__()
        self.setWindowTitle("AI Chatbot")
        
        # Create layout for the chatbot tab
        self.layout = QVBoxLayout()  # Initialize layout without passing self
        
        # Label for instructions
        self.instructions = QLabel("Enter your message to the AI:")
        self.layout.addWidget(self.instructions)
        
        # Text box for user input
        self.user_input = QTextEdit()
        self.layout.addWidget(self.user_input)
        
        # Button to send message
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Label to display AI response
        self.ai_response = QLabel("AI Response:")
        self.layout.addWidget(self.ai_response)

        # Set the layout for the tab
        self.setLayout(self.layout)

        # Initialize AI model and integration
        self.ai_model = AIModel()  # Create an instance of AIModel
        self.ai_integration = AIIntegration(self.ai_model)  # Create an instance of AIIntegration

    def send_message(self):
        """
        Process and send user message to AI system.
        
        This method:
        1. Retrieves message from input field
        2. Sends to AI for processing
        3. Displays the response
        4. Clears input for next message
        
        The AI response is formatted to highlight
        vulnerability-related information.
        """
        user_message = self.user_input.toPlainText()
        ai_response = self.get_ai_response(user_message)  # Get AI response
        self.ai_response.setText(f"AI: {ai_response}")  # Display AI response
        self.user_input.clear()  # Clear the input box after sending

    def get_ai_response(self, message):
        """
        Get AI response for a given user message.
        
        Parameters:
            message (str): User's input message
            
        Returns:
            str: Formatted AI response with vulnerability
                information, or error message if no relevant
                information is found
                
        Uses the AI integration system to process messages
        and format responses for security context.
        """
        # Use the AI integration to get a response based on user input
        response = self.ai_integration.get_response(message)
        if response:
            return f"Vulnerability Info: {response}"
        else:
            return "No information found for the given input."
