from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox)

class LoginDialog(QDialog):
    """
    Dialog for user authentication in the BugHunter application.
    
    This dialog provides a user interface for:
    - User login with username/password
    - New user registration
    - Token-based authentication management
    
    The dialog includes input validation and error handling for
    both login and registration operations.
    """
    
    def __init__(self, auth_manager, parent=None):
        """
        Initialize the login dialog.
        
        Parameters:
            auth_manager: Authentication manager instance for handling
                        login/register operations
            parent (QWidget, optional): Parent widget for this dialog
        """
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.user_token = None
        self.initUI()

    def initUI(self):
        """
        Initialize and set up the dialog's user interface.
        
        Creates and arranges:
        - Username input field
        - Password input field (with masked input)
        - Login button
        - Register button
        
        Sets up the layout and basic window properties.
        """
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        # Username input
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Register button
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        """
        Handle the login button click event.
        
        Validates input fields and attempts to log in the user:
        1. Checks for empty username/password
        2. Attempts authentication with provided credentials
        3. Verifies the received authentication token
        4. Stores the token on success
        
        Shows appropriate error messages for:
        - Missing credentials
        - Failed login attempts
        - Token verification failures
        """
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        result = self.auth_manager.login(username, password)
        if result['status'] == 'success':
            self.user_token = result['token']
            # Verify the token after successful login
            verification_result = self.auth_manager.verify_token(self.user_token)
            if verification_result['status'] != 'success':
                QMessageBox.warning(self, 'Token Verification Failed', verification_result['message'])
                return
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', result['message'])

    def handle_register(self):
        """
        Handle the register button click event.
        
        Validates input fields and attempts to register a new user:
        1. Checks for empty username/password
        2. Attempts to register with provided credentials
        3. Shows success/failure message
        
        Shows appropriate error messages for:
        - Missing credentials
        - Failed registration attempts
        """
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        result = self.auth_manager.register_user(username, password)
        if result['status'] == 'success':
            QMessageBox.information(self, 'Success', 'Registration successful. Please login.')
        else:
            QMessageBox.warning(self, 'Registration Failed', result['message'])

    def get_token(self):
        """
        Retrieve the authentication token after successful login.
        
        Returns:
            str: The user's authentication token if login was successful,
                 None otherwise
        """
        return self.user_token
