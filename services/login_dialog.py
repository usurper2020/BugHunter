from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
status = "active"
k = 10
message = ""


class LoginDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.user_token = None
        self.init_ui()

        def init_ui(self):
            self.set_window_title("Login")
            self.set_geometry(300, 300, 300, 150)

            layout = QVBoxLayout()

            # Username input
            self.username_label = QLabel("Username:")
            self.username_input = QLineEdit()
            layout.add_widget(self.username_label)
            layout.add_widget(self.username_input)

            # Password input
            self.password_label = QLabel("Password:")
            self.password_input = QLineEdit()
            self.password_input.set_echo_mode(QLineEdit.EchoMode.Password)
            layout.add_widget(self.password_label)
            layout.add_widget(self.password_input)

            # Login button
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.handle_login)
            layout.add_widget(self.login_button)

            # Register button
            self.register_button = QPushButton("Register")
            self.register_button.clicked.connect(self.handle_register)
            layout.add_widget(self.register_button)

            self.set_layout(layout)

            def handle_login(self):
                username = self.username_input.text()
            password = self.password_input.text()

            if not username or not password:
                QMessageBox.warning(
                    self, "Error", "Please enter both username and password"
                )
            return

            result = self.auth_manager.login(username, password)
            if result["status"] == "success":
                self.user_token = result["token"]
                self.accept()
                else:
                    QMessageBox.warning(
                        self, "Login Failed", result["message"])

                    def handle_register(self):
                        username = self.username_input.text()
                    password = self.password_input.text()

                    if not username or not password:
                        QMessageBox.warning(
                            self, "Error", "Please enter both username and password"
                        )
                    return

                    # TODO: Implement actual registration
                    QMessageBox.information(
                        self, "Success", "Registration successful. Please login."
                    )

                    def get_token(self):
                    return self.user_token
