# services/login_dialog.py
import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, auth_service):
        super().__init__()
        self.auth = auth_service
        self.logger = logging.getLogger('BugHunter.LoginDialog')
        self.token = None
        self.username = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the login dialog UI"""
        self.setWindowTitle("Login")
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(login_button)
        button_layout.addWidget(cancel_button)
        
        # Add all layouts to main layout
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(button_layout)
        
        # Set dialog layout
        self.setLayout(layout)
        
        # Connect signals
        login_button.clicked.connect(self.handle_login)
        cancel_button.clicked.connect(self.reject)
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        """Handle login button click"""
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            
            # Validate input
            if not username or not password:
                QMessageBox.warning(
                    self,
                    "Input Error",
                    "Please enter both username and password."
                )
                return
            
            # Attempt login
            success = self.auth.login(username, password)
            
            if success:
                self.username = username
                self.token = self.auth.token
                self.logger.info(f"User '{username}' logged in successfully")
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Login Failed",
                    "Invalid username or password."
                )
                self.password_input.clear()
                
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            QMessageBox.critical(
                self,
                "Login Error",
                f"An error occurred during login: {str(e)}"
            )
