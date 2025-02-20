from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSlot
import os
from typing import Dict, List

class ToolTab(QWidget):
    def __init__(self, tool_manager=None):  # Make tool_manager parameter optional
        super().__init__()
        self.tool_manager = tool_manager
        self.github_tools = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Search section
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search GitHub tools...")
        
        self.language_filter = QComboBox()
        self.language_filter.addItems(['All', 'Python', 'Go', 'Ruby', 'JavaScript', 'Rust'])
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_tools)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.language_filter)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Results section
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Tool Name", "Language", "Stars", "Description", "Actions"
        ])
        layout.addWidget(self.results_table)

        # Installed tools section
        layout.addWidget(QLabel("Installed Tools"))
        
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(4)
        self.installed_table.setHorizontalHeaderLabels([
            "Tool", "Status", "Version", "Actions"
        ])
        layout.addWidget(self.installed_table)

        self.setLayout(layout)

    def search_tools(self):
        """Search for tools on GitHub"""
        if not self.tool_manager:
            QMessageBox.warning(self, "Warning", "Tool manager not initialized")
            return
            
        query = self.search_input.text().strip()
        if not query:
            return

        try:
            language = self.language_filter.currentText()
            if language == 'All':
                language = None
                
            result = self.tool_manager.search_github_tools(query, language)
            
            if result['status'] == 'success':
                self.display_search_results(result['results'])
            else:
                QMessageBox.warning(self, "Error", result['message'])
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to search tools: {str(e)}")

    def display_search_results(self, items: List[Dict]):
        """Display search results in the table"""
        self.results_table.setRowCount(0)
        self.github_tools = items

        for row, item in enumerate(items):
            self.results_table.insertRow(row)
            
            self.results_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.results_table.setItem(row, 1, QTableWidgetItem(item.get('language', 'N/A')))
            self.results_table.setItem(row, 2, QTableWidgetItem(str(item.get('stargazers_count', 0))))
            self.results_table.setItem(row, 3, QTableWidgetItem(item.get('description', '')))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            
            install_btn = QPushButton("Install")
            install_btn.clicked.connect(lambda checked, x=row: self.install_tool(x))
            
            actions_layout.addWidget(install_btn)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.results_table.setCellWidget(row, 4, actions_widget)

    def install_tool(self, row: int):
        """Install selected tool"""
        if not self.tool_manager:
            QMessageBox.warning(self, "Warning", "Tool manager not initialized")
            return
            
        try:
            tool = self.github_tools[row]
            result = self.tool_manager.install_github_tool(
                tool['html_url'],
                'main.py'  # Default main file, can be improved
            )
            
            if result['status'] == 'success':
                QMessageBox.information(self, "Success", result['message'])
                self.load_installed_tools()
            else:
                QMessageBox.warning(self, "Error", result['message'])
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to install tool: {str(e)}")

    def load_installed_tools(self):
        """Load and display installed tools"""
        if not self.tool_manager:
            return
            
        try:
            result = self.tool_manager.list_tools()
            
            if result['status'] != 'success':
                return
                
            self.installed_table.setRowCount(0)
            
            for tool_name, info in result['tools'].items():
                row = self.installed_table.rowCount()
                self.installed_table.insertRow(row)
                
                self.installed_table.setItem(row, 0, QTableWidgetItem(tool_name))
                self.installed_table.setItem(row, 1, QTableWidgetItem(info.get('status', 'Unknown')))
                self.installed_table.setItem(row, 2, QTableWidgetItem(info.get('version', 'Unknown')))
                
                # Action buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                
                uninstall_btn = QPushButton("Uninstall")
                uninstall_btn.clicked.connect(lambda checked, t=tool_name: self.uninstall_tool(t))
                
                actions_layout.addWidget(uninstall_btn)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                
                self.installed_table.setCellWidget(row, 3, actions_widget)
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load installed tools: {str(e)}")

    def uninstall_tool(self, tool_name: str):
        """Uninstall a tool"""
        if not self.tool_manager:
            return
            
        try:
            result = self.tool_manager.uninstall_tool(tool_name)
            
            if result['status'] == 'success':
                QMessageBox.information(self, "Success", result['message'])
                self.load_installed_tools()
            else:
                QMessageBox.warning(self, "Error", result['message'])
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to uninstall tool: {str(e)}")
