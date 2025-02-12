"""
AI Chat interface tab for the BugHunter application.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QComboBox, QFrame, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QColor, QSyntaxHighlighter, QTextCharFormat

class CodeHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for code snippets in chat messages."""
    
    def __init__(self, parent=None):
        """Initialize the syntax highlighter."""
        super().__init__(parent)
        self.highlighting_rules = []

        # Define formats for different syntax elements
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keywords = [
            "def", "class", "import", "from", "return", "if", "else", "elif",
            "try", "except", "finally", "for", "while", "in", "is", "not",
            "and", "or", "True", "False", "None"
        ]
        for word in keywords:
            self.highlighting_rules.append((f"\\b{word}\\b", keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
        self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.highlighting_rules.append((r"#[^\n]*", comment_format))

    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text."""
        for pattern, format in self.highlighting_rules:
            expression = pattern
            index = text.find(expression)
            while index >= 0:
                length = len(expression)
                self.setFormat(index, length, format)
                index = text.find(expression, index + length)

class AIChatTab(QWidget):
    """Main chat interface tab for AI interaction."""
    
    def __init__(self, ai_system=None):
        """Initialize the chat interface tab."""
        super().__init__()
        self.ai_system = ai_system
        self.chat_history = []
        self.logger = logging.getLogger('BugHunter.AIChatTab')
        self.init_ui()

    def init_ui(self):
        """Set up the user interface components."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Top controls layout
        top_controls = QHBoxLayout()
        
        # API Selection
        api_label = QLabel("AI Model:")
        api_label.setStyleSheet("color: #CCCCCC;")
        self.api_selector = QComboBox()
        self.api_selector.setStyleSheet(""" 
            QComboBox {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.api_selector.addItems(['OpenAI', 'CodeGPT'])
        self.api_selector.currentTextChanged.connect(self.change_api)
        
        # Add to top controls
        top_controls.addWidget(api_label)
        top_controls.addWidget(self.api_selector)
        
        # Website URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter target website URL for analysis")
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
                padding: 5px;
                min-width: 300px;
            }
        """)
        top_controls.addWidget(self.url_input)
        
        # Analyze button
        self.analyze_button = QPushButton("Analyze Website")
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.analyze_button.clicked.connect(self.analyze_website)
        top_controls.addWidget(self.analyze_button)
        
        top_controls.addStretch()
        
        # Clear chat button
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.setStyleSheet(""" 
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #BB2D3B;
            }
        """)
        self.clear_button.clicked.connect(self.clear_chat)
        top_controls.addWidget(self.clear_button)
        
        layout.addLayout(top_controls)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(""" 
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet(""" 
            QFrame {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
                border-radius: 5px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("Type your message here... (Ctrl+Enter to send)")
        self.input_field.setStyleSheet(""" 
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(""" 
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
            QPushButton:disabled {
                background-color: #6C757D;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_frame)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(""" 
            QLabel {
                color: #6C757D;
                padding: 5px;
                font-style: italic;
            }
        """)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def change_api(self, api_name):
        """Switch between different AI API backends."""
        if self.ai_system:
            self.ai_system.set_api(api_name.lower())
            self.status_label.setText(f"Switched to {api_name} API")
            self.logger.info(f"API changed to {api_name}")
        else:
            self.status_label.setText("AI system not initialized")
            self.logger.error("Cannot change API: AI system not initialized")

    def clear_chat(self):
        """Clear the chat history and display."""
        self.chat_display.clear()
        self.chat_history.clear()
        self.status_label.setText("Chat cleared")
        self.logger.info("Chat cleared")

    def analyze_website(self):
        """Analyze the target website for vulnerabilities."""
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a website URL")
            return
            
        self.analyze_button.setEnabled(False)
        self.status_label.setText("Analyzing website...")
        
        try:
            if self.ai_system:
                # Get website analysis
                analysis = self.ai_system.analyze_website(url)
                
                if analysis['status'] == 'success':
                    # Format analysis results
                    message = "🔍 Website Analysis Results:\n\n"
                    
                    # Technologies detected
                    message += "📊 Detected Technologies:\n"
                    for tech in analysis['technologies']:
                        message += f"• {tech}\n"
                    message += "\n"
                    
                    # Potential vulnerabilities
                    message += "⚠️ Potential Vulnerabilities:\n"
                    for vuln in analysis['potential_vulnerabilities']:
                        message += f"• {vuln['type']} ({vuln['severity']} severity)\n"
                        message += f"  - Location: {vuln['location']}\n"
                        message += f"  - Confidence: {vuln['confidence']}\n\n"
                    
                    # Template suggestions
                    message += "🎯 Recommended Nuclei Templates:\n"
                    for template in analysis['template_suggestions']:
                        message += f"• {template['id']} ({template['severity']})\n"
                        message += f"  - {template['description']}\n\n"
                    
                    # Security recommendations
                    message += "💡 Security Recommendations:\n"
                    for rec in analysis['recommendations']:
                        message += f"• {rec}\n"
                    
                    # Add analysis to chat
                    self.chat_history.append({"role": "assistant", "content": message})
                    self.chat_display.append(self.format_message("assistant", message))
                    
                    # Update status
                    self.status_label.setText("Analysis complete")
                else:
                    raise Exception(analysis['message'])
            else:
                raise Exception("AI system not initialized")
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Analysis error: {error_msg}")
            error_html = (
                '<div style="margin-bottom: 10px; background-color: #DC3545; padding: 10px; border-radius: 5px;">'
                f'<span style="color: #FFFFFF;">Error: {error_msg}</span>'
                '</div>'
            )
            self.chat_display.append(error_html)
            self.status_label.setText("Analysis failed")
            
        finally:
            self.analyze_button.setEnabled(True)

    def send_message(self):
        """Process and send a user message to the AI."""
        user_message = self.input_field.toPlainText().strip()
        if not user_message:
            return

        self.send_button.setEnabled(False)
        self.input_field.clear()
        self.status_label.setText("Processing message...")

        # Add user message to chat
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_display.append(self.format_message("user", user_message))

        try:
            if self.ai_system:
                # Process message with enhanced context
                context = {
                    'message': user_message,
                    'chat_history': self.chat_history[-10:],  # Last 10 messages for context
                    'current_url': self.url_input.text().strip(),
                    'current_analysis': self.get_current_analysis()
                }
                
                # Get AI response
                response = self.ai_system.process_message(context)
                
                # Add response to chat
                self.chat_history.append({"role": "assistant", "content": response})
                self.chat_display.append(self.format_message("assistant", response))
                self.status_label.setText("Ready")
            else:
                raise Exception("AI system not initialized")
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"AI error: {error_msg}")
            error_html = (
                '<div style="margin-bottom: 10px; background-color: #DC3545; padding: 10px; border-radius: 5px;">'
                f'<span style="color: #FFFFFF;">Error: {error_msg}</span>'
                '</div>'
            )
            self.chat_display.append(error_html)
            self.status_label.setText("Error occurred")
        
        finally:
            self.send_button.setEnabled(True)

    def get_current_analysis(self):
        """Get the current website analysis context if available."""
        url = self.url_input.text().strip()
        if url and self.ai_system:
            try:
                return self.ai_system.get_cached_analysis(url)
            except:
                return None
        return None

    def format_message(self, role, content):
        """Format a chat message for display."""
        if role == "user":
            return (
                '<div style="margin-bottom: 10px; background-color: #2D2D2D; padding: 10px; border-radius: 5px;">'
                '<span style="color: #4EC9B0; font-weight: bold;">You:</span><br>'
                f'<span style="color: #FFFFFF;">{content}</span>'
                '</div>'
            )
        else:
            return (
                '<div style="margin-bottom: 10px; background-color: #1E1E1E; padding: 10px; border-radius: 5px;">'
                '<span style="color: #569CD6; font-weight: bold;">AI:</span><br>'
                f'<span style="color: #FFFFFF;">{content}</span>'
                '</div>'
            )

    def keyPressEvent(self, event):
        """Handle keyboard input events."""
        if event.key() == Qt.Key.Key_Return and (
            event.modifiers() & Qt.KeyboardModifier.ControlModifier or
            event.modifiers() & Qt.KeyboardModifier.MetaModifier
        ):
            self.send_message()
        else:
            super().keyPressEvent(event)
