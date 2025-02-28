from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from ..services.simple_auth import SimpleAuth


class LoginDialog(QDialog):
    def __init__(self, auth_service: SimpleAuth, parent=None):

        super().__init__(parent)
        self.auth_service = auth_service
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("BugHunter Login")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        
        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_button)
        
        # Register Button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_registration)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)

    def show_registration(self):
        """Show the registration dialog"""
        from ..gui.registration_dialog import RegistrationDialog
        registration_dialog = RegistrationDialog(self.auth_service, self)
        if registration_dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Success", "Registration successful! Please login.")

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        try:
            # Attempt login using SimpleAuth
            login_result = self.auth_service.login(username, password)

            
            if login_result:
                self.accept()  # Close dialog with success
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login error: {str(e)}")
