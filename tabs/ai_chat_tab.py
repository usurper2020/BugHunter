# tabs/ai_chat_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                            QPushButton, QComboBox)
from services.ai_service import AIService

class AIChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ai_service = AIService()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # AI Provider Selection
        ai_selection_layout = QHBoxLayout()
        ai_selection_layout.addWidget(QLabel("Select AI Provider:"))
        self.ai_provider = QComboBox()
        self.ai_provider.addItems(["OpenAI", "CodeGPT", "BugHunter"])
        self.ai_provider.currentTextChanged.connect(self.change_ai_provider)
        ai_selection_layout.addWidget(self.ai_provider)
        layout.addLayout(ai_selection_layout)
        
        # Provider Info
        self.provider_info = QLabel()
        self.update_provider_info("OpenAI")  # Default provider
        layout.addWidget(self.provider_info)
        
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

    def change_ai_provider(self, provider: str):
        """Change the AI provider and update the info display."""
        self.ai_service.api_type = provider.lower()
        self.update_provider_info(provider)
        self.chat_history.append(f"Switched to {provider} AI provider")

    def update_provider_info(self, provider: str):
        """Update the provider information display."""
        info = {
            "OpenAI": "Cloud-based AI with advanced natural language understanding",
            "CodeGPT": "Specialized code analysis and security-focused AI",
            "BugHunter": "Local AI with built-in security patterns and quick response time"
        }
        self.provider_info.setText(f"Current Provider: {provider}\n{info[provider]}")

    def send_message(self):
        """Send the user's message to the selected AI provider and display the response."""
        user_message = self.input_field.toPlainText().strip()
        if user_message:
            self.chat_history.append(f"You: {user_message}")
            try:
                response = self.ai_service.analyze_vulnerability({
                    'query': user_message,
                    'scan_type': 'chat',
                    'target': 'user_query'
                })
                
                if isinstance(response, dict):
                    # Format the response based on the provider
                    if self.ai_service.api_type == 'bughunter':
                        ai_response = self._format_bughunter_response(response)
                    else:
                        ai_response = response['analysis'].get('summary', str(response))
                else:
                    ai_response = str(response)
                
                self.chat_history.append(f"AI: {ai_response}")
            except Exception as e:
                self.chat_history.append(f"Error: {str(e)}")
            finally:
                self.input_field.clear()

    def _format_bughunter_response(self, response: Dict[str, Any]) -> str:
        """Format BugHunter's response for display."""
        if response['status'] == 'success':
            return "\n".join([
                "Analysis Results:",
                f"- Technologies detected: {', '.join(response['technologies'])}",
                f"- Vulnerabilities found: {len(response['vulnerabilities'])}",
                "Recommendations:",
                *[f"- {rec}" for rec in response['recommendations']]
            ])
        return f"Analysis failed: {response.get('message', 'Unknown error')}"
