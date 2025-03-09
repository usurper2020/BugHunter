from PyQt6.QtWidgets import (
QCheckBox,
QGroupBox,
QHBoxLayout,
QLabel,
QLineEdit,
QPushButton,
QSlider,
QVBoxLayout,
QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from typing import Any, Dict, Callable
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
value = None
k = 10
items = []
tools = []


"""
GUI Tab Generator for the BugHunter application.

Handles creation of dynamic GUI tabs for converted tools using PyQt6.
"""

class GUITabGenerator:
    """
    Generates GUI tabs for converted tools using PyQt6.
    """

    def __init__(self, tool_name: str, tool_metadata: Dict[str, Any], execute_callback: Callable):
        self.config_manager = config_manager
        self.tabs = {}

    def create_tab(
        self, tool_name: str, tool_metadata: Dict[str, Any], execute_callback: Callable
    ) -> QWidget:
        """
        Create a GUI tab for a converted tool.

        Args:
            tool_name: Name of the tool
            tool_metadata: Metadata about the tool
            execute_callback: Function to call when tool is executed

        Returns:
            QWidget containing the tool's GUI
        """
        tab = QWidget()
        layout = QVBoxLayout()

        # Add tool name label
        name_label = QLabel(f"Tool: {tool_name}")
        layout.add_widget(name_label)

        # Add description
        desc_label = QLabel(tool_metadata.get("description", ""))
        layout.add_widget(desc_label)

        # Add execute button
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(
            lambda: execute_callback(tool_name))
        layout.add_widget(execute_button)

        # Add settings controls
        if "settings" in tool_metadata:
            self._add_settings_controls(
                layout, tool_metadata["settings"])

        tab.set_layout(layout)
        self.tabs[tool_name] = tab
        return tab

    def _add_settings_controls(
        self, layout: QVBoxLayout, settings: Dict[str, Any]
    ) -> None:
        """
        Add settings controls to the tab.

        Args:
            layout: The layout to add controls to
            settings: Dictionary of tool settings
        """
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        for setting, value in settings.items():
            row = QWidget()
            row_layout = QHBoxLayout()
            row.set_layout(row_layout)

            label = QLabel(setting)
            row_layout.add_widget(label)

            if isinstance(value, bool):
                control = QCheckBox()
                control.set_checked(value)
            elif isinstance(value, (int, float)):
                control = QSlider(
                    Qt.Orientation.Horizontal)
                control.set_minimum(0)
                control.set_maximum(100)
                control.set_value(int(value))
            else:
                control = QLineEdit(str(value))

            row_layout.add_widget(control)
            settings_layout.add_widget(row)

        settings_group.set_layout(
            settings_layout)
        layout.add_widget(settings_group)

    def get_tab(self, _tool_name: str) -> QWidget:
        """
        Get an existing tab for a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            The tool's tab widget
        """
        return self.tabs.get(tool_name)

    def remove_tab(self, _tool_name: str) -> None:
        """
        Remove a tool's tab.

        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tabs:
            del self.tabs[tool_name]