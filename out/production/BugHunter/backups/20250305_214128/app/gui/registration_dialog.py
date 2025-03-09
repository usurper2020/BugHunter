from app.services.simple_auth import SimpleAuth  # Changed from relative import
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


class RegistrationDialog(QDialog):
    def __init__(self, _auth_service: SimpleAuth, _parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.setup_ui()

        def setup_ui(self):
            self.set_window_title("User Registration")
            self.set_fixed_size(350, 250)

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

            # Confirm Password
            self.confirm_password_label = QLabel("Confirm Password:")
            self.confirm_password_input = QLineEdit()
            self.confirm_password_input.set_echo_mode(
                QLineEdit.EchoMode.Password)
            layout.add_widget(self.confirm_password_label)
            layout.add_widget(self.confirm_password_input)

            # Email
            self.email_label = QLabel("Email:")
            self.email_input = QLineEdit()
            layout.add_widget(self.email_label)
            layout.add_widget(self.email_input)

            # Register Button
            self.register_button = QPushButton("Register")
            self.register_button.clicked.connect(self.attempt_registration)
            layout.add_widget(self.register_button)

            self.set_layout(layout)

            def attempt_registration(self):
                username = self.username_input.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()
            email = self.email_input.text()

            if not username or not password or not confirm_password or not email:
                QMessageBox.warning(
                    self, "Registration Failed", "All fields are required")
            return

            if password != confirm_password:
                QMessageBox.warning(
                    self, "Registration Failed", "Passwords do not match")
            return

            try:
                # Attempt registration using SimpleAuth
                registration_result = self.auth_service.register(
                    username=username, password=password
                )

                if registration_result:
                    QMessageBox.information(
                        self, "Registration Success", "Account created successfully"
                    )
                    self.accept()
                    else:
                        QMessageBox.warning(
                            self, "Registration Failed", "Username or email already exists"
                        )

                        except Exception as e:
                            QMessageBox.critical(
                                self, "Error", f"Registration error: {str(e)}")
