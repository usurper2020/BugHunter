"""
AI Chat tab for the BugHunter application.

This tab retains and expands the existing AI chat feature, providing
an interface for interacting with the AI system.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from services.ai_system import AISystem

class AIChatTab(QWidget):
    """
    Tab widget providing AI chatbot functionality.
    
    This widget creates a simple chat interface with:
    - Text input area for user messages
    - Send button for message submission
    - Response display area for AI output
    - Integration with backend AI systems
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.ai_system = AISystem()

    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Chat history display
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)
        
        # Input area
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        layout.addWidget(QLabel("Your message:"))
        layout.addWidget(self.input_field)
        
        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)
        
        self.setLayout(layout)

    def send_message(self):
        """Send the user's message to the AI system and display the response."""
        user_message = self.input_field.toPlainText().strip()
        if user_message:
            self.chat_history.append(f"You: {user_message}")
            response = self.ai_system.get_response(user_message)
            self.chat_history.append(f"AI: {response}")
            self.input_field.clear()
