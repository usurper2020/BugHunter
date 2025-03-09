from app.services.tool_manager import ToolManager
from PyQt6.QtWidgets import (
QHBoxLayout,
QHeaderView,
QLabel,
QLineEdit,
QMessageBox,
QProgressBar,
QPushButton,
QTableWidget,
QTableWidgetItem,
QVBoxLayout,
QWidget,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
url = ""
k = 10
message = ""
tools = []
"""
Tool Manager Tab Module.

This module provides the GUI interface for managing security tools in the BugHunter application.
It allows users to search, install, remove, and manage various security tools through
a user-friendly interface.

    Classes:
    ToolManagerTab: Main class implementing the tool management interface.
    """

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
            self.search_input.set_placeholder_text(
            "Search for tools...")
            search_layout.add_widget(self.search_input)

            self.search_button = QPushButton("Search")
            search_layout.add_widget(self.search_button)
            layout.add_layout(search_layout)

            # Results table
            self.results_table = QTableWidget()
            self.results_table.set_column_count(3)
            self.results_table.set_horizontal_header_labels(
            ["Name", "Description", "Action"])
            header = self.results_table.horizontal_header()
            header.set_section_resize_mode(
            0, QHeaderView.ResizeMode.ResizeToContents)
            header.set_section_resize_mode(
            1, QHeaderView.ResizeMode.Stretch)
            header.set_section_resize_mode(
            2, QHeaderView.ResizeMode.ResizeToContents)
            layout.add_widget(self.results_table)

            # Progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.set_visible(False)
            layout.add_widget(self.progress_bar)

            # Status bar
            self.status_bar = QLabel()
            self.status_bar.set_style_sheet(
            "color: #2196f3; font-weight: bold;")
            layout.add_widget(self.status_bar)

            # Installed tools section
            layout.add_widget(QLabel("Installed Tools:"))
            self.installed_table = QTableWidget()
            self.installed_table.set_column_count(2)
            self.installed_table.set_horizontal_header_labels(
            ["Tool Name", "Action"])
            header = self.installed_table.horizontal_header()
            header.set_section_resize_mode(
            0, QHeaderView.ResizeMode.Stretch)
            header.set_section_resize_mode(
            1, QHeaderView.ResizeMode.ResizeToContents)
            layout.add_widget(self.installed_table)

            self.set_layout(layout)

                def connect_signals(self):
                """
                Connect UI signals to appropriate slots.

                Sets up the event handling for user interactions.
                """
                self.search_button.clicked.connect(
                self.search_tools)
                self.tool_manager.progress_signal.connect(
                self.update_progress)
                self.tool_manager.status_signal.connect(
                self.update_status)
                self.tool_manager.error_signal.connect(
                self.show_error)

                self.tool_manager.status_signal.connect(
                self.update_status)
                self.tool_manager.error_signal.connect(
                self.show_error)

                    def search_tools(self):
                    """
                    Search for tools and update the results table.

                    self.tool_manager.progress_signal.connect(self.update_progress)
                    self.tool_manager.status_signal.connect(self.update_status)
                    self.tool_manager.error_signal.connect(self.show_error)
                                    try:
                                    # Description
                                    desc_item = QTableWidgetItem(tool.get('description', 'No description'))
                                    desc_item.set_flags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                                    self.results_table.set_item(row, 1, desc_item)

                                    # Install button
                                    install_btn = QPushButton("Install")
                                    install_btn.clicked.connect(lambda checked, t=tool: self.install_tool(t))
                                    self.results_table.set_cell_widget(row, 2, install_btn)
                                        except Exception as e:
                                        self.show_error(f"Search error: {str(e)}")
                                        Install a selected tool.

                                            Args:
                                            tool (dict): Dictionary containing tool information from search results.

                                            Handles the installation process and updates the UI accordingly.
                                            """
                        try:
                        self.progress_bar.set_visible(True)
                        result = self.tool_manager.download_tool(
                        tool["html_url"])
                            if result["status"] == "success":
                            self.update_status(
                            f"Installed: {result['tool_name']}")
                            self.refresh_tool_list()
                                except Exception as e:
                                self.show_error(
                                f"Installation error: {str(e)}")
                                    finally:
                                    self.progress_bar.set_visible(
                                    False)

                                        def refresh_tool_list(self):
                                        """
                                        Refresh the list of installed tools.

                                        Updates the installed tools table with current information.
                                        """
                                        tools = self.tool_manager.list_tools()
                                        self.installed_table.set_row_count(
                                        len(tools))

                                            for row, tool_name in enumerate(tools):
                                            # Tool name
                                            name_item = QTableWidgetItem(
                                            tool_name)
                                            name_item.set_flags(
                                            name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                                            self.installed_table.set_item(
                                            row, 0, name_item)

                                            # Remove button
                                            remove_btn = QPushButton(
                                            "Remove")
                                            remove_btn.clicked.connect(
                                            lambda checked, t=tool_name: self.remove_tool(t))
                                            self.installed_table.set_cell_widget(
                                            row, 1, remove_btn)

                                                def remove_tool(self, tool_name):
                                                """
                                                Remove an installed tool.

                                                                    Args:
                                                                    tool_name (str): Name of the tool to remove.

                                                                    Prompts for confirmation before removing the tool.
                                                                    """
                                                                    reply = QMessageBox.question(
                                                                    self,
                                                                    "Confirm Deletion",
                                                                    f"Are you sure you want to remove {tool_name}?",
                                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                                    )

                                                    if reply == QMessageBox.StandardButton.Yes:
                                                        try:
                                                        result = self.tool_manager.delete_tool(
                                                        tool_name)
                                                        self.update_status(
                                                        result)
                                                        self.refresh_tool_list()
                                                            except Exception as e:
                                                            self.show_error(
                                                            f"Error removing tool: {str(e)}")

                                                                def update_progress(self, message, percentage):
                                                                """
                                                                Update progress bar and status.

                                                                                        Args:
                                                                                        message (str): Progress message to display.
                                                                                        percentage (int): Progress percentage (0-100).
                                                                                        """
                                                                                        self.progress_bar.set_value(
                                                                                        percentage)
                                                                                        self.update_status(
                                                                                        f"{message} ({percentage}%)")

                                                                    def update_status(self, message):
                                                                    """
                                                                    Update status message.

                                                                                                Args:
                                                                                                message (str): Status message to display.
                                                                                                """
                                                                                                self.status_bar.set_text(
                                                                                                message)

                                                                        def show_error(self, message):
                                                                        """
                                                                        Show error message to the user.

                                                                                                        Args:
                                                                                                        message (str): Error message to display.
                                                                                                        """
                                                                                                        QMessageBox.critical(
                                                                                                        self, "Error", message)