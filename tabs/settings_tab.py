"""
Settings Tab Module.

This module provides the GUI interface for managing application settings in the BugHunter application.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import Qt

class SettingsTab(QWidget):
    """
    Settings tab for the BugHunter application.

    This tab allows users to configure application settings such as API keys, preferences, and more.
    """

    def __init__(self, parent=None):
        """
        Initialize the SettingsTab.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface components.
        """
        layout = QVBoxLayout()

        # API Key Section
        api_key_layout = QVBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key here...")
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)

        # Preferences Section
        preferences_layout = QVBoxLayout()
        preferences_layout.addWidget(QLabel("Preferences:"))
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        preferences_layout.addWidget(self.dark_mode_checkbox)
        layout.addLayout(preferences_layout)

        # Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        """
        Save the current settings.
        """
        api_key = self.api_key_input.text()
        dark_mode = self.dark_mode_checkbox.isChecked()
        
        # Save settings logic here (e.g., save to config file or database)
        print(f"API Key: {api_key}, Dark Mode: {dark_mode}")
