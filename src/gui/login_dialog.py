from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import logging
import time
from src.gui.registration_dialog import RegistrationDialog  # Changed from relative import
from src.services.simple_auth import SimpleAuth  # Changed from relative import



class LoginDialog(QDialog):
    WINDOW_TITLE = "BugHunter Login"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 200

    def __init__(self, auth_service: SimpleAuth, parent=None):
        """
        Initialize the LoginDialog.

        :param auth_service: An instance of SimpleAuth for handling authentication.
        :param parent: The parent widget of this dialog. Defaults to None.
        """
        super().__init__(parent)
        self.auth_service = auth_service
        self.setup_ui()
        self.failed_attempts = 0
        self.last_failed_attempt_time = None

    def setup_ui(self):
        """
        Sets up the user interface for the login dialog.
        """
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        layout = QVBoxLayout()
        self.setup_username_input(layout)
        self.setup_password_input(layout)
        self.setup_buttons(layout)
        self.setLayout(layout)

    def setup_username_input(self, layout):
        """
        Sets up the username input fields.
        """
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

    def setup_password_input(self, layout):
        """
        Sets up the password input fields.
        """
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

    def setup_buttons(self, layout):
        """
        Sets up the login and register buttons.
        """
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.attempt_login)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_registration)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

    def show_registration(self):
        """
        Displays the registration dialog to the user.

        This method creates an instance of the RegistrationDialog class,
        passing the authentication service and the current instance as
        parameters. It then executes the dialog, allowing the user to
        register a new account.

        Returns:
            None
        """
        registration_dialog = RegistrationDialog(self.auth_service, self)
        registration_dialog.exec()  # Show the registration dialog

    def attempt_login(self):
        """
        Attempts to log in the user with the provided username and password.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if self.auth_service.authenticate(username, password):
                QMessageBox.information(self, "Success", "Login successful!")
                logging.info("User '%s' logged in successfully.", username)
            else:
                self.failed_attempts += 1
                self.last_failed_attempt_time = time.time()
                QMessageBox.critical(self, "Error", "Invalid username or password.")
                self.handle_invalid_login(username)
        except ValueError as e:
            self.handle_invalid_login(username, str(e))

    def handle_invalid_login(self, username, error_message="Invalid username or password."):
        """
        Handles invalid login attempts by logging the error and notifying the user.

        :param username: The username used in the login attempt.
        :param error_message: The error message to display to the user.
        """
        self.password_input.clear()
        QMessageBox.critical(self, "Error", f"An unexpected error occurred: {error_message}")
        logging.error("An unexpected error occurred during login attempt for username: %s - %s", username, error_message, exc_info=True)
