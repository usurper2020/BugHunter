from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ResetPasswordDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.initUI()

    def initUI(self):
        self.setGeometry(
            300,  # x position
            300,  # y position
            300,  # width
            150   # height
        )
        layout = QVBoxLayout()
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Reset Password button
        self.reset_password_button = QPushButton('Reset Password')
        self.reset_password_button.clicked.connect(self.handle_reset_password)
        layout.addWidget(self.reset_password_button)

        self.setLayout(layout)

    def handle_reset_password(self):
        email = self.email_input.text()
        try:
            if self.auth_manager.reset_password(email):
                QMessageBox.information(self, 'Success', 'Password reset link sent to your email.')
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Email not found')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
