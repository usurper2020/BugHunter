from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

key = ""
k = 10
"""
Settings Tab Module.

This module provides the GUI interface for managing application settings in the BugHunter application.
"""


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
            api_key_layout.add_widget(QLabel("API Key:"))
            self.api_key_input = QLineEdit()
            self.api_key_input.set_placeholder_text(
                "Enter your API key here...")
            api_key_layout.add_widget(self.api_key_input)
            layout.add_layout(api_key_layout)

            # Preferences Section
            preferences_layout = QVBoxLayout()
            preferences_layout.add_widget(QLabel("Preferences:"))
            self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
            preferences_layout.add_widget(self.dark_mode_checkbox)
            layout.add_layout(preferences_layout)

            # Save Button
            save_button = QPushButton("Save Settings")
            save_button.clicked.connect(self.save_settings)
            layout.add_widget(save_button)

            self.set_layout(layout)

            def save_settings(self):
                """
                Save the current settings.
                """
                api_key = self.api_key_input.text()
                dark_mode = self.dark_mode_checkbox.is_checked()

                # Save settings logic here (e.g., save to config file or database)
                print(f"API Key: {api_key}, Dark Mode: {dark_mode}")
