import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QComboBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QColor, QSyntaxHighlighter, QTextCharFormat

class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
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
            self.highlighting_rules.append((
                f"\\b{word}\\b", keyword_format
            ))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((
            r'"[^"\\]*(\\.[^"\\]*)*"', string_format
        ))
        self.highlighting_rules.append((
            r"'[^'\\]*(\\.[^'\\]*)*'", string_format
        ))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.highlighting_rules.append((
            r"#[^\n]*", comment_format
        ))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = pattern
            index = text.find(expression)
            while index >= 0:
                length = len(expression)
                self.setFormat(index, length, format)
                index = text.find(expression, index + length)

class AIChatTab(QWidget):
    def __init__(self, openai_client=None, codegpt_client=None):
        super().__init__()
        self.openai_client = openai_client
        self.codegpt_client = codegpt_client
        self.current_client = 'openai' if openai_client else 'codegpt'
        self.chat_history = []
        self.logger = logging.getLogger('BugHunter.AIChatTab')
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.show_typing_indicator)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Top controls layout
        top_controls = QHBoxLayout()
        
        # API Selection
        api_label = QLabel("API:")
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
        if self.openai_client:
            self.api_selector.setCurrentText('OpenAI')
        elif self.codegpt_client:
            self.api_selector.setCurrentText('CodeGPT')
        self.api_selector.currentTextChanged.connect(self.change_api)
        
        # Model Selection
        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #CCCCCC;")
        self.model_selector = QComboBox()
        self.model_selector.setStyleSheet(self.api_selector.styleSheet())
        self.update_model_list()
        
        # Add to top controls
        top_controls.addWidget(api_label)
        top_controls.addWidget(self.api_selector)
        top_controls.addWidget(model_label)
        top_controls.addWidget(self.model_selector)
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

    def update_model_list(self):
        self.model_selector.clear()
        if self.current_client == 'openai':
            self.model_selector.addItems(['gpt-3.5-turbo', 'gpt-4'])
        else:  # codegpt
            self.model_selector.addItems(['gpt-3.5-turbo'])

    def change_api(self, api_name):
        self.current_client = api_name.lower()
        self.update_model_list()
        self.status_label.setText(f"Switched to {api_name} API")
        self.logger.info(f"API changed to {api_name}")

    def clear_chat(self):
        self.chat_display.clear()
        self.chat_history.clear()
        self.status_label.setText("Chat cleared")
        self.logger.info("Chat cleared")

    def format_message(self, role, content):
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

    def show_typing_indicator(self):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml('<span style="color: #6C757D;">AI is typing...</span><br>')
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def send_message(self):
        user_message = self.input_field.toPlainText().strip()
        if not user_message:
            return

        self.send_button.setEnabled(False)
        self.status_label.setText("Sending message...")
        self.input_field.clear()

        # Add user message to chat
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_display.append(self.format_message("user", user_message))

        # Show typing indicator
        self.typing_timer.start(500)

        try:
            if self.current_client == 'openai' and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model_selector.currentText(),
                    messages=self.chat_history
                )
                ai_response = response.choices[0].message.content
            elif self.current_client == 'codegpt' and self.codegpt_client:
                response = self.codegpt_client.create_completion(
                    messages=self.chat_history
                )
                ai_response = response['choices'][0]['message']['content']
            else:
                raise Exception("No API client configured for the selected service.")
            
            # Stop typing indicator
            self.typing_timer.stop()
            
            # Add AI response to chat
            self.chat_history.append({"role": "assistant", "content": ai_response})
            self.chat_display.append(self.format_message("assistant", ai_response))
            self.status_label.setText("Ready")
            
        except Exception as e:
            self.typing_timer.stop()
            error_msg = str(e)
            self.logger.error(f"API error: {error_msg}")
            error_html = (
                '<div style="margin-bottom: 10px; background-color: #DC3545; padding: 10px; border-radius: 5px;">'
                '<span style="color: #FFFFFF;">Error: {error_msg}</span>'
                '</div>'
            )
            self.chat_display.append(error_html)
            self.status_label.setText("Error occurred")
        
        finally:
            self.send_button.setEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and (
            event.modifiers() & Qt.KeyboardModifier.ControlModifier or
            event.modifiers() & Qt.KeyboardModifier.MetaModifier
        ):
            self.send_message()
        else:
            super().keyPressEvent(event)
