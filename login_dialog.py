from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox)

class LoginDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.user_token = None
        self.initUI()

    def initUI(self):
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
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        result = self.auth_manager.login(username, password)
        if result['status'] == 'success':
            self.user_token = result['token']
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', result['message'])

    def handle_register(self):
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
        return self.user_token
