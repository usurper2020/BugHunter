from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from backend.ai_integration import AIIntegration  # Import the AIIntegration class
from backend.models import AIModel  # Import the AIModel class

class AIChatbotTab(QWidget):
    def __init__(self):
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
        user_message = self.user_input.toPlainText()
        ai_response = self.get_ai_response(user_message)  # Get AI response
        self.ai_response.setText(f"AI: {ai_response}")  # Display AI response
        self.user_input.clear()  # Clear the input box after sending

    def get_ai_response(self, message):
        # Use the AI integration to get a response based on user input
        response = self.ai_integration.get_response(message)
        if response:
            return f"Vulnerability Info: {response}"
        else:
            return "No information found for the given input."
