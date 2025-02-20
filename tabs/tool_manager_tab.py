from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
import os
from tool_manager import ToolManager

class ToolManagerTab(QWidget):
    """
    A tab widget for managing security tools in the BugHunter application.
    
    This tab provides functionality to:
    - Download and install security tools from GitHub
    - View and manage installed tools
    - Monitor tool installation progress
    - Display tool-related notifications and errors
    """
    
    def __init__(self, tool_manager=None):
        """
        Initialize the ToolManagerTab with an optional tool manager instance.

        This constructor sets up the tool management interface and initializes
        the underlying tool management system.

        Parameters:
            tool_manager (ToolManager, optional): An instance of ToolManager for handling
                tool-related operations. If not provided, a new instance will be created.
        """
        super().__init__()
        # Use provided tool_manager or create new one
        self.tool_manager = tool_manager if tool_manager is not None else ToolManager()
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the tool manager tab.
        """
        layout = QVBoxLayout()

        # Search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for bug bounty tools (e.g., 'scanner', 'recon')")
        self.search_input.textChanged.connect(self.search_tools)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Tool results table
        self.tools_table = QTableWidget()
        self.tools_table.setColumnCount(4)
        self.tools_table.setHorizontalHeaderLabels(["Name", "Description", "Category", "Action"])
        header = self.tools_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.tools_table)

        # Installed tools section
        layout.addWidget(QLabel("Installed Tools:"))
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(2)
        self.installed_table.setHorizontalHeaderLabels(["Tool Name", "Action"])
        header = self.installed_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.installed_table)

        # Status output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(100)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.refresh_tool_list()
        
        # Show initial suggestions
        self.search_tools("")

    def refresh_tool_list(self):
        """
        Refresh the list of installed tools.
        """
        tools = self.tool_manager.list_tools()
        self.installed_table.setRowCount(len(tools))
        
        for row, tool_name in enumerate(tools):
            # Tool name
            name_item = QTableWidgetItem(tool_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.installed_table.setItem(row, 0, name_item)
            
            # Delete button
            delete_btn = QPushButton("Remove")
            delete_btn.clicked.connect(lambda checked, t=tool_name: self.delete_tool(t))
            self.installed_table.setCellWidget(row, 1, delete_btn)
            
    def delete_tool(self, tool_name):
        """
        Delete an installed tool.
        """
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                   f'Are you sure you want to remove {tool_name}?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.tool_manager.delete_tool(tool_name)
                self.output_text.append(result)
                self.refresh_tool_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def search_tools(self, query):
        """
        Search for tools and update the results table.
        """
        results = self.tool_manager.search_tool(query)
        self.tools_table.setRowCount(len(results))
        
        for row, tool in enumerate(results):
            # Name
            name_item = QTableWidgetItem(tool['name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tools_table.setItem(row, 0, name_item)
            
            # Description
            desc_item = QTableWidgetItem(tool['description'])
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tools_table.setItem(row, 1, desc_item)
            
            # Category
            category = tool.get('category', 'External Tool')
            cat_item = QTableWidgetItem(category)
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tools_table.setItem(row, 2, cat_item)
            
            # Install button
            install_btn = QPushButton("Install")
            install_btn.clicked.connect(lambda checked, t=tool: self.download_tool(t))
            self.tools_table.setCellWidget(row, 3, install_btn)

    def download_tool(self, tool):
        """
        Download and install a security tool.
        """
        try:
            identifier = tool['name'] if tool.get('type') == 'suggested' else tool.get('url', '')
            result = self.tool_manager.download_tool(identifier)
            
            if result['status'] == 'success':
                self.output_text.append(f"✅ {result['message']}")
            elif result['status'] == 'warning':
                self.output_text.append(f"⚠️ {result['message']}")
            else:
                self.output_text.append(f"❌ {result['message']}")
            
            self.refresh_tool_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
