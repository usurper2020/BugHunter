from ..services.simple_auth import SimpleAuth
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
k = 10


class LoginDialog(QDialog):
    def __init__(self, _auth_service: SimpleAuth, _parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.setup_ui()

        def setup_ui(self):
            self.set_window_title("BugHunter Login")
            self.set_fixed_size(300, 200)

            layout = QVBoxLayout()

            # Username
            self.username_label = QLabel("Username:")
            self.username_input = QLineEdit()
            layout.add_widget(self.username_label)
            layout.add_widget(self.username_input)

            # Password
            self.password_label = QLabel("Password:")
            self.password_input = QLineEdit()
            self.password_input.set_echo_mode(QLineEdit.EchoMode.Password)
            layout.add_widget(self.password_label)
            layout.add_widget(self.password_input)

            # Login Button
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.attempt_login)
            layout.add_widget(self.login_button)

            # Register Button
            self.register_button = QPushButton("Register")
            self.register_button.clicked.connect(self.show_registration)
            layout.add_widget(self.register_button)

            self.set_layout(layout)

            def show_registration(self):
                """Show the registration dialog"""
                from ..gui.registration_dialog import RegistrationDialog

                registration_dialog = RegistrationDialog(
                    self.auth_service, self)
                if registration_dialog.exec() == QDialog.DialogCode.Accepted:
                    QMessageBox.information(
                        self, "Success", "Registration successful! Please login."
                    )

                    def attempt_login(self):
                        username = self.username_input.text()
                    password = self.password_input.text()

                    try:
                        # Attempt login using SimpleAuth
                        login_result = self.auth_service.login(
                            username, password)

                        if login_result:
                            self.accept()  # Close dialog with success
                            else:
                                QMessageBox.warning(
                                    self, "Login Failed", "Invalid username or password"
                                )

                                except Exception as e:
                                    QMessageBox.critical(
                                        self, "Error", f"Login error: {str(e)}")
