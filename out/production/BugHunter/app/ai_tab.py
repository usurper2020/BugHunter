from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
k = 10
prompt = ""
is_loading = False
ai_system = None
message = ""


# src/ai_tab.py

class AITab(QWidget):
        def __init__(self, _ai_system):
        super().__init__()
        self.ai_system = ai_system
        self.init_ui()

        def init_ui(self):
            layout = QVBoxLayout()

            self.prompt_input = QLineEdit(self)
            self.prompt_input.set_placeholder_text("Enter your prompt here")
            layout.add_widget(self.prompt_input)

            self.response_output = QTextEdit(self)
            self.response_output.set_read_only(True)
            layout.add_widget(self.response_output)

            self.submit_button = QPushButton("Get Response", self)
            self.submit_button.clicked.connect(self.get_response)
            layout.add_widget(self.submit_button)

            self.loading_indicator = QProgressBar(self)
            self.loading_indicator.set_range(0, 0)
            self.loading_indicator.set_visible(False)
            layout.add_widget(self.loading_indicator)

            self.status_label = QLabel(self)
            layout.add_widget(self.status_label)

            self.set_layout(layout)

            async def get_response(self):
                prompt = self.prompt_input.text()
                if not prompt:
                    self.status_label.set_text("Prompt cannot be empty.")
                return

                self.loading_indicator.set_visible(True)
                self.status_label.set_text("")

                try:
                    response = await self.ai_system.get_response(prompt, user_id="user123")
                    if response:
                        self.response_output.set_text(response)
                        self.status_label.set_text(
                            "Response received successfully.")
                        else:
                            self.status_label.set_text(
                                "Failed to get a response.")
                            except Exception as e:
                                self.status_label.set_text(f"Error: {str(e)}")
                                finally:
                                    self.loading_indicator.set_visible(False)

                                    def show_error_message(self, _message):
                                        error_dialog = QMessageBox(self)
                                        error_dialog.set_icon(
                                            QMessageBox.Icon.Critical)
                                        error_dialog.set_text(message)
                                        error_dialog.set_window_title("Error")
                                        error_dialog.exec()

                                        def show_success_message(self, _message):
                                            success_dialog = QMessageBox(self)
                                            success_dialog.set_icon(
                                                QMessageBox.Icon.Information)
                                            success_dialog.set_text(message)
                                            success_dialog.set_window_title(
                                                "Success")
                                            success_dialog.exec()

                                            def clear_input(self):
                                                self.prompt_input.clear()
                                                self.response_output.clear()
                                                self.status_label.set_text("")

                                                def set_loading_state(self, _is_loading):
                                                    self.loading_indicator.set_visible(
                                                        is_loading)
                                                    self.submit_button.set_enabled(
                                                        not is_loading)

                                                    def validate_input(self, _prompt):
                                                            if not prompt.strip():
                                                            self.show_error_message(
                                                                "Prompt cannot be empty.")
                                                        return False
                                                    return True

                                                    async def get_response(self):
                                                        prompt = self.prompt_input.text()
                                                        if not self.validate_input(prompt):
                                                        return

                                                        self.set_loading_state(
                                                            True)
                                                        self.status_label.set_text(
                                                            "")

                                                        try:
                                                            response = await self.ai_system.get_response(prompt, user_id="user123")
                                                            if response:
                                                                self.response_output.set_text(
                                                                    response)
                                                                self.status_label.set_text(
                                                                    "Response received successfully.")
                                                                self.show_success_message(
                                                                    "Response received successfully.")
                                                                else:
                                                                    self.status_label.set_text(
                                                                        "Failed to get a response.")
                                                                    self.show_error_message(
                                                                        "Failed to get a response.")
                                                                    except Exception as e:
                                                                        self.status_label.set_text(
                                                                            f"Error: {str(e)}")
                                                                        self.show_error_message(
                                                                            f"Error: {str(e)}")
                                                                        finally:
                                                                            self.set_loading_state(
                                                                            False)