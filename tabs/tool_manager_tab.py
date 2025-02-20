"""
Tool Manager Tab Module.

This module provides the GUI interface for managing security tools in the BugHunter application.
It allows users to search, install, remove, and manage various security tools through
a user-friendly interface.

Classes:
    ToolManagerTab: Main class implementing the tool management interface.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from tool_manager import ToolManager
import os

class ToolManagerTab(QWidget):
    """
    Main tool management tab for the BugHunter application.

    This class provides a graphical interface for managing security tools,
    including searching, installing, removing, and tracking progress.

    Attributes:
        tool_manager (ToolManager): Instance of ToolManager for backend operations.
        search_input (QLineEdit): Input field for search queries.
        search_button (QPushButton): Button to initiate searches.
        results_table (QTableWidget): Table displaying search results.
        progress_bar (QProgressBar): Progress indicator for operations.
        installed_table (QTableWidget): Table listing installed tools.
    """

    def __init__(self, tool_manager=None, parent=None):
        """
        Initialize the ToolManagerTab.

        Args:
            tool_manager (ToolManager, optional): ToolManager instance. Defaults to None.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.tool_manager = tool_manager if tool_manager else ToolManager()
        self.init_ui()
        self.connect_signals()
        self.refresh_tool_list()

    def init_ui(self):
        """
        Initialize the user interface components.

        Sets up the layout, widgets, and initial state of the tab.
        """
        layout = QVBoxLayout()

        # Search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for tools...")
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Name", "Description", "Action"])
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.results_table)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status bar
        self.status_bar = QLabel()
        self.status_bar.setStyleSheet("color: #2196f3; font-weight: bold;")
        layout.addWidget(self.status_bar)

        # Installed tools section
        layout.addWidget(QLabel("Installed Tools:"))
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(2)
        self.installed_table.setHorizontalHeaderLabels(["Tool Name", "Action"])
        header = self.installed_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.installed_table)

        self.setLayout(layout)

    def connect_signals(self):
        """
        Connect UI signals to appropriate slots.

        Sets up the event handling for user interactions.
        """
        self.search_button.clicked.connect(self.search_tools)
        self.tool_manager.progress_signal.connect(self.update_progress)
        self.tool_manager.status_signal.connect(self.update_status)
        self.tool_manager.error_signal.connect(self.show_error)

    def search_tools(self):
        """
        Search for tools and update the results table.

        Executes a search query and displays the results in the table.
        Handles any errors that occur during the search process.
        """
        query = self.search_input.text()
        try:
            results = self.tool_manager.search_github(query)
            self.results_table.setRowCount(len(results))
            
            for row, tool in enumerate(results):
                # Name
                name_item = QTableWidgetItem(tool['name'])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.results_table.setItem(row, 0, name_item)
                
                # Description
                desc_item = QTableWidgetItem(tool.get('description', 'No description'))
                desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.results_table.setItem(row, 1, desc_item)
                
                # Install button
                install_btn = QPushButton("Install")
                install_btn.clicked.connect(lambda checked, t=tool: self.install_tool(t))
                self.results_table.setCellWidget(row, 2, install_btn)
        except Exception as e:
            self.show_error(f"Search error: {str(e)}")

    def install_tool(self, tool):
        """
        Install a selected tool.

        Args:
            tool (dict): Dictionary containing tool information from search results.

        Handles the installation process and updates the UI accordingly.
        """
        try:
            self.progress_bar.setVisible(True)
            result = self.tool_manager.download_tool(tool['html_url'])
            if result['status'] == 'success':
                self.update_status(f"Installed: {result['tool_name']}")
                self.refresh_tool_list()
        except Exception as e:
            self.show_error(f"Installation error: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)

    def refresh_tool_list(self):
        """
        Refresh the list of installed tools.

        Updates the installed tools table with current information.
        """
        tools = self.tool_manager.list_tools()
        self.installed_table.setRowCount(len(tools))
        
        for row, tool_name in enumerate(tools):
            # Tool name
            name_item = QTableWidgetItem(tool_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.installed_table.setItem(row, 0, name_item)
            
            # Remove button
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, t=tool_name: self.remove_tool(t))
            self.installed_table.setCellWidget(row, 1, remove_btn)

    def remove_tool(self, tool_name):
        """
        Remove an installed tool.

        Args:
            tool_name (str): Name of the tool to remove.

        Prompts for confirmation before removing the tool.
        """
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                   f'Are you sure you want to remove {tool_name}?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.tool_manager.delete_tool(tool_name)
                self.update_status(result)
                self.refresh_tool_list()
            except Exception as e:
                self.show_error(f"Error removing tool: {str(e)}")

    def update_progress(self, message, percentage):
        """
        Update progress bar and status.

        Args:
            message (str): Progress message to display.
            percentage (int): Progress percentage (0-100).
        """
        self.progress_bar.setValue(percentage)
        self.update_status(f"{message} ({percentage}%)")

    def update_status(self, message):
        """
        Update status message.

        Args:
            message (str): Status message to display.
        """
        self.status_bar.setText(message)

    def show_error(self, message):
        """
        Show error message to the user.

        Args:
            message (str): Error message to display.
        """
        QMessageBox.critical(self, "Error", message)
