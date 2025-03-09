from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
link = ""
k = 10


class ResetPasswordDialog(QDialog):
    def __init__(self, _auth_manager, _parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.init_ui()

        def init_ui(self):
            self.set_geometry(
                300, 300, 300, 150  # x position  # y position  # width  # height
            )
            layout = QVBoxLayout()
            self.email_label = QLabel("Email:")
            self.email_input = QLineEdit()
            layout.add_widget(self.email_label)
            layout.add_widget(self.email_input)

            # Reset Password button
            self.reset_password_button = QPushButton("Reset Password")
            self.reset_password_button.clicked.connect(
                self.handle_reset_password)
            layout.add_widget(self.reset_password_button)

            self.set_layout(layout)

            def handle_reset_password(self):
                email = self.email_input.text()
                try:
                    if self.auth_manager.reset_password(email):
                        QMessageBox.information(
                            self, "Success", "Password reset link sent to your email."
                        )
                        self.accept()
                        else:
                            QMessageBox.warning(
                                self, "Error", "Email not found")
                            except Exception as e:
                                QMessageBox.critical(
                                    self, "Error", f"An error occurred: {e}")
