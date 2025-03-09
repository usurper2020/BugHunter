# tabs/tool_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSlot
import aiohttp
import asyncio
import subprocess
import os
from typing import List, Dict
import json

class ToolTab(QWidget):
    def __init__(self, tool_manager):
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
        self.search_input.returnPressed.connect(self.search_tools)
        
        self.language_filter = QComboBox()
        self.language_filter.addItems(['All', 'Python', 'Go', 'Ruby', 'JavaScript', 'Rust'])
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_tools)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.language_filter)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Search results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Tool Name", "Language", "Stars", "Description", "Actions"
        ])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.results_table)

        # Installed tools section
        layout.addWidget(QLabel("Installed Tools"))
        
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(4)
        self.installed_table.setHorizontalHeaderLabels([
            "Tool", "Status", "Version", "Path"
        ])
        layout.addWidget(self.installed_table)

        self.setLayout(layout)
        self.load_installed_tools()

    @pyqtSlot()
    async def search_tools(self):
        """Search for tools on GitHub"""
        query = self.search_input.text().strip()
        if not query:
            return

        self.progress.setVisible(True)
        self.search_button.setEnabled(False)
        
        try:
            language_filter = self.language_filter.currentText()
            if language_filter != 'All':
                query += f" language:{language_filter}"

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.github.com/search/repositories",
                    params={
                        "q": query + " topic:security",
                        "sort": "stars",
                        "order": "desc"
                    },
                    headers={"Accept": "application/vnd.github.v3+json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.display_search_results(data['items'])
                    else:
                        raise Exception(f"GitHub API returned status {response.status}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search tools: {e}")

        finally:
            self.progress.setVisible(False)
            self.search_button.setEnabled(True)

    def display_search_results(self, items: List[Dict]):
        """Display search results in the table"""
        self.results_table.setRowCount(0)
        self.github_tools = items

        for row, item in enumerate(items):
            self.results_table.insertRow(row)
            
            # Tool name with link
            name_item = QTableWidgetItem(item['name'])
            name_item.setData(Qt.ItemDataRole.UserRole, item['html_url'])
            self.results_table.setItem(row, 0, name_item)
            
            # Language
            self.results_table.setItem(row, 1, QTableWidgetItem(item.get('language', 'N/A')))
            
            # Stars
            self.results_table.setItem(row, 2, QTableWidgetItem(str(item['stargazers_count'])))
            
            # Description
            self.results_table.setItem(row, 3, QTableWidgetItem(item.get('description', '')))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            
            install_btn = QPushButton("Install")
            install_btn.clicked.connect(lambda checked, x=row: self.install_tool(x))
            
            convert_btn = QPushButton("Convert to Python")
            convert_btn.clicked.connect(lambda checked, x=row: self.convert_to_python(x))
            
            actions_layout.addWidget(install_btn)
            actions_layout.addWidget(convert_btn)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.results_table.setCellWidget(row, 4, actions_widget)

    async def install_tool(self, row: int):
        """Install selected tool"""
        tool = self.github_tools[row]
        try:
            self.progress.setVisible(True)
            
            # Clone repository
            repo_path = os.path.join('tools', tool['name'])
            process = await asyncio.create_subprocess_exec(
                'git', 'clone', tool['clone_url'], repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

            if process.returncode == 0:
                # Install dependencies if Python
                if tool.get('language') == 'Python':
                    requirements_file = os.path.join(repo_path, 'requirements.txt')
                    if os.path.exists(requirements_file):
                        process = await asyncio.create_subprocess_exec(
                            'pip', 'install', '-r', requirements_file,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()

                QMessageBox.information(self, "Success", f"Tool {tool['name']} installed successfully!")
                self.load_installed_tools()
            else:
                raise Exception("Failed to clone repository")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to install tool: {e}")

        finally:
            self.progress.setVisible(False)

    async def convert_to_python(self, row: int):
        """Convert tool to Python"""
        tool = self.github_tools[row]
        if tool.get('language') == 'Python':
            QMessageBox.information(self, "Info", "Tool is already in Python!")
            return

        try:
            self.progress.setVisible(True)
            
            # Use OpenAI to help with conversion
            response = await self.get_conversion_help(tool)
            
            # Save the converted code
            output_dir = os.path.join('tools', f"{tool['name']}_python")
            os.makedirs(output_dir, exist_ok=True)
            
            with open(os.path.join(output_dir, 'converted.py'), 'w') as f:
                f.write(response)
                
            QMessageBox.information(self, "Success", 
                f"Tool converted to Python! Check {output_dir}/converted.py")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert tool: {e}")

        finally:
            self.progress.setVisible(False)

    async def get_conversion_help(self, tool: Dict) -> str:
        """Get help from OpenAI for code conversion"""
        try:
            # Get the source code
            async with aiohttp.ClientSession() as session:
                async with session.get(tool['contents_url'].replace('{+path}', '')) as response:
                    if response.status == 200:
                        contents = await response.json()
                        
                        # Use OpenAI to convert the code
                        response = await self.tool_manager.convert_code_to_python(
                            contents['content'],
                            tool.get('language', 'unknown')
                        )
                        return response
                    else:
                        raise Exception(f"Failed to get source code: {response.status}")

        except Exception as e:
            raise Exception(f"Failed to get conversion help: {e}")

    def load_installed_tools(self):
        """Load and display installed tools"""
        try:
            tools_dir = 'tools'
            if not os.path.exists(tools_dir):
                os.makedirs(tools_dir)

            self.installed_table.setRowCount(0)
            
            for tool_name in os.listdir(tools_dir):
                row = self.installed_table.rowCount()
                self.installed_table.insertRow(row)
                
                self.installed_table.setItem(row, 0, QTableWidgetItem(tool_name))
                self.installed_table.setItem(row, 1, QTableWidgetItem("Installed"))
                
                # Try to get version
                try:
                    version = self.get_tool_version(tool_name)
                    self.installed_table.setItem(row, 2, QTableWidgetItem(version))
                except:
                    self.installed_table.setItem(row, 2, QTableWidgetItem("Unknown"))
                
                self.installed_table.setItem(row, 3, QTableWidgetItem(
                    os.path.join(tools_dir, tool_name)
                ))

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load installed tools: {e}")

    def get_tool_version(self, tool_name: str) -> str:
        """Get tool version"""
        try:
            result = subprocess.run(
                [os.path.join('tools', tool_name, tool_name), '--version'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() or "Unknown"
        except:
            return "Unknown"
