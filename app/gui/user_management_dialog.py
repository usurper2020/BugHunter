from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from typing import List
from dataclasses import dataclass
import json
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
status = "active"
k = 10
message = ""
items = []


class UserManagementDialog(QDialog):
        def __init__(self, _auth_manager, _parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.init_ui()

        def init_ui(self):
            self.set_window_title("User Management")
            self.set_geometry(300, 300, 600, 400)

            layout = QVBoxLayout()

            # User Creation Section
            creation_layout = QHBoxLayout()

            # Username input
            username_layout = QVBoxLayout()
            self.username_label = QLabel("Username:")
            self.username_input = QLineEdit()
            username_layout.add_widget(self.username_label)
            username_layout.add_widget(self.username_input)
            creation_layout.add_layout(username_layout)

            # Password input
        password_layout = QVBoxLayout()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.set_echo_mode(QLineEdit.EchoMode.Password)
    password_layout.add_widget(self.password_label)
password_layout.add_widget(self.password_input)
creation_layout.add_layout(password_layout)

# Role selection
role_layout = QVBoxLayout()
self.role_label = QLabel("Role:")
self.role_combo = QComboBox()
self.role_combo.add_items(["admin", "user", "guest"])
role_layout.add_widget(self.role_label)
role_layout.add_widget(self.role_combo)
creation_layout.add_layout(role_layout)

# Create user button
self.create_button = QPushButton("Create User")
self.create_button.clicked.connect(self.create_user)
creation_layout.add_widget(self.create_button)

layout.add_layout(creation_layout)

# User List Section
self.users_table = QTableWidget()
self.users_table.set_column_count(3)
self.users_table.set_horizontal_header_labels(
    ["Username", "Role", "Actions"])
layout.add_widget(self.users_table)

# Refresh button
self.refresh_button = QPushButton("Refresh User List")
self.refresh_button.clicked.connect(self.refresh_users)
layout.add_widget(self.refresh_button)

self.set_layout(layout)
self.refresh_users()

def create_user(self):
    """Create a new user"""
    username = self.username_input.text()
password = self.password_input.text()
role = self.role_combo.current_text()

if not username or not password:
    QMessageBox.warning(
        self, "Error", "Please enter both username and password"
    )
return

result = self.auth_manager.register_user(
    username, password, role)
if result["status"] == "success":
    QMessageBox.information(
        self, "Success", "User created successfully")
    self.username_input.clear()
    self.password_input.clear()
    self.refresh_users()
    else:
        QMessageBox.warning(self, "Error", result["message"])

        def refresh_users(self):
            """Refresh the user list"""
            try:
                    with open(self.auth_manager.users_file, "r", encoding="utf-8") as f:
                    users = json.load(f)

                    self.users_table.set_row_count(len(users))
                    for row, (username, data) in enumerate(users.items()):
                            # Username
                        self.users_table.set_item(
                            row, 0, QTableWidgetItem(username))
                        # Role
                        self.users_table.set_item(
                            row, 1, QTableWidgetItem(data["role"]))
                        # Actions
                        delete_button = QPushButton("Delete")
                        delete_button.clicked.connect(
                            lambda checked, u=username: self.delete_user(
                            u)
                        )
                        self.users_table.set_cell_widget(
                            row, 2, delete_button)

                        self.users_table.resize_columns_to_contents()

                        except Exception as e:
                            QMessageBox.warning(
                                self, "Error", f"Failed to load users: {str(e)}")

                            def delete_user(self, _username):
                                """Delete a user"""
                                reply = QMessageBox.question(
                                    self,
                                    "Confirm Delete",
                                    f"Are you sure you want to delete user {username}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                )

                                if reply == QMessageBox.StandardButton.Yes:
                                        try:
                                            with open(self.auth_manager.users_file, "r", encoding="utf-8") as f:
                                            users = json.load(
                                                f)

                                            if username in users:
                                                del users[username]

                                                with open(self.auth_manager.users_file, "w", encoding="utf-8") as f:
                                                    json.dump(
                                                        users, f)

                                                    QMessageBox.information(
                                                        self, "Success", "User deleted successfully"
                                                    )
                                                    self.refresh_users()
                                                    else:
                                                        QMessageBox.warning(
                                                            self, "Error", "User not found")

                                                        except Exception as e:
                                                            QMessageBox.warning(
                                                            self, "Error", f"Failed to delete user: {str(e)}")