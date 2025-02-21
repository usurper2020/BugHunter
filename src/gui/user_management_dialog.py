import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QComboBox, QMessageBox,
                            QTableWidget, QTableWidgetItem)

class UserManagementDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle('User Management')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        # User Creation Section
        creation_layout = QHBoxLayout()

        # Username input
        username_layout = QVBoxLayout()
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)
        creation_layout.addLayout(username_layout)

        # Password input
        password_layout = QVBoxLayout()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        creation_layout.addLayout(password_layout)

        # Role selection
        role_layout = QVBoxLayout()
        self.role_label = QLabel('Role:')
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'user', 'guest'])
        role_layout.addWidget(self.role_label)
        role_layout.addWidget(self.role_combo)
        creation_layout.addLayout(role_layout)

        # Create user button
        self.create_button = QPushButton('Create User')
        self.create_button.clicked.connect(self.create_user)
        creation_layout.addWidget(self.create_button)

        layout.addLayout(creation_layout)

        # User List Section
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Role', 'Actions'])
        layout.addWidget(self.users_table)

        # Refresh button
        self.refresh_button = QPushButton('Refresh User List')
        self.refresh_button.clicked.connect(self.refresh_users)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.refresh_users()

    def create_user(self):
        """Create a new user"""
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return

        result = self.auth_manager.register_user(username, password, role)
        if result['status'] == 'success':
            QMessageBox.information(self, 'Success', 'User created successfully')
            self.username_input.clear()
            self.password_input.clear()
            self.refresh_users()
        else:
            QMessageBox.warning(self, 'Error', result['message'])

    def refresh_users(self):
        """Refresh the user list"""
        try:
            with open(self.auth_manager.users_file, 'r') as f:
                users = json.load(f)

            self.users_table.setRowCount(len(users))
            for row, (username, data) in enumerate(users.items()):
                # Username
                self.users_table.setItem(row, 0, QTableWidgetItem(username))
                # Role
                self.users_table.setItem(row, 1, QTableWidgetItem(data['role']))
                # Actions
                delete_button = QPushButton('Delete')
                delete_button.clicked.connect(lambda checked, u=username: self.delete_user(u))
                self.users_table.setCellWidget(row, 2, delete_button)

            self.users_table.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load users: {str(e)}')

    def delete_user(self, username):
        """Delete a user"""
        reply = QMessageBox.question(self, 'Confirm Delete',
                                   f'Are you sure you want to delete user {username}?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with open(self.auth_manager.users_file, 'r') as f:
                    users = json.load(f)

                if username in users:
                    del users[username]

                    with open(self.auth_manager.users_file, 'w') as f:
                        json.dump(users, f)

                    QMessageBox.information(self, 'Success', 'User deleted successfully')
                    self.refresh_users()
                else:
                    QMessageBox.warning(self, 'Error', 'User not found')

            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to delete user: {str(e)}')
