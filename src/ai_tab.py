# src/ai_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QProgressBar, QMessageBox
import asyncio

class AITab(QWidget):
    def __init__(self, ai_system):
        super().__init__()
        self.ai_system = ai_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.prompt_input = QLineEdit(self)
        self.prompt_input.setPlaceholderText("Enter your prompt here")
        layout.addWidget(self.prompt_input)

        self.response_output = QTextEdit(self)
        self.response_output.setReadOnly(True)
        layout.addWidget(self.response_output)

        self.submit_button = QPushButton("Get Response", self)
        self.submit_button.clicked.connect(self.get_response)
        layout.addWidget(self.submit_button)

        self.loading_indicator = QProgressBar(self)
        self.loading_indicator.setRange(0, 0)
        self.loading_indicator.setVisible(False)
        layout.addWidget(self.loading_indicator)

        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    async def get_response(self):
        prompt = self.prompt_input.text()
        if not prompt:
            self.status_label.setText("Prompt cannot be empty.")
            return

        self.loading_indicator.setVisible(True)
        self.status_label.setText("")

        try:
            response = await self.ai_system.get_response(prompt, user_id="user123")
            if response:
                self.response_output.setText(response)
                self.status_label.setText("Response received successfully.")
            else:
                self.status_label.setText("Failed to get a response.")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
        finally:
            self.loading_indicator.setVisible(False)

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

    def show_success_message(self, message):
        success_dialog = QMessageBox(self)
        success_dialog.setIcon(QMessageBox.Icon.Information)
        success_dialog.setText(message)
        success_dialog.setWindowTitle("Success")
        success_dialog.exec()

    def clear_input(self):
        self.prompt_input.clear()
        self.response_output.clear()
        self.status_label.setText("")

    def set_loading_state(self, is_loading):
        self.loading_indicator.setVisible(is_loading)
        self.submit_button.setEnabled(not is_loading)

    def validate_input(self, prompt):
        if not prompt.strip():
            self.show_error_message("Prompt cannot be empty.")
            return False
        return True

    async def get_response(self):
        prompt = self.prompt_input.text()
        if not self.validate_input(prompt):
            return

        self.set_loading_state(True)
        self.status_label.setText("")

        try:
            response = await self.ai_system.get_response(prompt, user_id="user123")
            if response:
                self.response_output.setText(response)
                self.status_label.setText("Response received successfully.")
                self.show_success_message("Response received successfully.")
            else:
                self.status_label.setText("Failed to get a response.")
                self.show_error_message("Failed to get a response.")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.show_error_message(f"Error: {str(e)}")
        finally:
            self.set_loading_state(False)
