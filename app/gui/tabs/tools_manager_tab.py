"""
Tool Manager Tab for BugHunter.
"""

import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from PyQt6.QtCore import QObject, Qt, pyqtSignal
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


class ToolManager(QObject):
    progress_signal = pyqtSignal(str, int)
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("BugHunter.ToolManager")
        self.tools_dir = Path("tools")
        self.tools_dir.mkdir(exist_ok=True)
        self.tools_config = {}
        self.active_processes: Dict[str, subprocess.Popen] = {}

    def search_github(self, query: str) -> List[Dict[str, Any]]:
        """Search for tools on GitHub"""
        # Dummy implementation for example purposes
        return [
            {
                "name": "Tool1",
                "description": "Description for Tool1",
                "html_url": "http://example.com/tool1",
            },
            {
                "name": "Tool2",
                "description": "Description for Tool2",
                "html_url": "http://example.com/tool2",
            },
        ]

    def download_tool(self, url: str) -> Dict[str, Any]:
        """Download a tool from a given URL"""
        # Dummy implementation for example purposes
        tool_name = url.split("/")[-1]
        return {"status": "success", "tool_name": tool_name}

    def list_tools(self) -> List[str]:
        """List installed tools"""
        # Dummy implementation for example purposes
        return ["Tool1", "Tool2"]

    def delete_tool(self, tool_name: str) -> str:
        """Delete an installed tool"""
        # Dummy implementation for example purposes
        return f"Deleted: {tool_name}"

    def initialize(self) -> bool:
        """Initialize tool manager and load configurations"""
        try:
            # Load tool configurations
            config_file = Path("config/tools.yml")
            if config_file.exists():
                with open(config_file, "r") as f:
                    self.tools_config = yaml.safe_load(f)

            # Verify tool installations
            self._verify_installations()

            self.logger.info("Tool manager initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Tool manager initialization failed: {str(e)}")
            return False

    def _verify_installations(self):
        """Verify tool installations and their dependencies"""
        for tool_name, tool_info in self.tools_config.items():
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                self.logger.warning(f"Tool not installed: {tool_name}")
                continue

            # Verify dependencies
            if "dependencies" in tool_info:
                for dep in tool_info["dependencies"]:
                    try:
                        subprocess.run(["which", dep], check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        self.logger.warning(
                            f"Missing dependency for {tool_name}: {dep}"
                        )

    def install_tool(self, tool_name: str) -> bool:
        """Install a security tool"""
        try:
            if tool_name not in self.tools_config:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_info = self.tools_config[tool_name]
            tool_path = self.tools_dir / tool_name

            # Create tool directory
            tool_path.mkdir(exist_ok=True)

            # Clone repository if provided
            if "repository" in tool_info:
                subprocess.run(
                    ["git", "clone", tool_info["repository"], str(tool_path)],
                    check=True,
                )

            # Run installation commands
            if "install_commands" in tool_info:
                for cmd in tool_info["install_commands"]:
                    subprocess.run(cmd, shell=True, cwd=str(tool_path), check=True)

            self.logger.info(f"Tool installed successfully: {tool_name}")
            return True

        except Exception as e:
            self.logger.error(f"Tool installation failed - {tool_name}: {str(e)}")
            return False

    def update_tool(self, tool_name: str) -> bool:
        """Update a security tool"""
        try:
            tool_path = self.tools_dir / tool_name
            if not tool_path.exists():
                raise ValueError(f"Tool not installed: {tool_name}")

            # Pull latest changes if git repository
            if (tool_path / ".git").exists():
                subprocess.run(["git", "pull"], cwd=str(tool_path), check=True)

            # Run update commands if specified
            tool_info = self.tools_config.get(tool_name, {})
            if "update_commands" in tool_info:
                for cmd in tool_info["update_commands"]:
                    subprocess.run(cmd, shell=True, cwd=str(tool_path), check=True)

            self.logger.info(f"Tool updated successfully: {tool_name}")
            return True

        except Exception as e:
            self.logger.error(f"Tool update failed - {tool_name}: {str(e)}")
            return False

    def execute_tool(self, tool_name: str, args: List[str]) -> Dict[str, Any]:
        """Execute a security tool with given arguments"""
        try:
            if tool_name not in self.tools_config:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_info = self.tools_config[tool_name]
            tool_path = self.tools_dir / tool_name

            # Build command
            cmd = [tool_info["executable"]] + args

            # Start process
            process = subprocess.Popen(
                cmd,
                cwd=str(tool_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Store process
            self.active_processes[tool_name] = process

            # Wait for completion
            stdout, stderr = process.communicate()

            # Remove from active processes
            del self.active_processes[tool_name]

            return {
                "status": "success" if process.returncode == 0 else "error",
                "returncode": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
            }

        except Exception as e:
            self.logger.error(f"Tool execution failed - {tool_name}: {str(e)}")
            return {"status": "error", "error": str(e)}

    def stop_tool(self, tool_name: str) -> bool:
        """Stop a running tool process"""
        try:
            if tool_name in self.active_processes:
                process = self.active_processes[tool_name]
                process.terminate()
                process.wait(timeout=5)
                del self.active_processes[tool_name]
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to stop tool - {tool_name}: {str(e)}")
            return False

    def get_tool_status(self, tool_name: str) -> Dict[str, Any]:
        """Get status of a tool"""
        try:
            if tool_name not in self.tools_config:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_path = self.tools_dir / tool_name

            return {
                "installed": tool_path.exists(),
                "running": tool_name in self.active_processes,
                "version": self._get_tool_version(tool_name),
                "last_update": self._get_last_update(tool_name),
            }

        except Exception as e:
            self.logger.error(f"Failed to get tool status - {tool_name}: {str(e)}")
            return {"error": str(e)}

    def _get_tool_version(self, tool_name: str) -> Optional[str]:
        """Get version of installed tool"""
        try:
            tool_info = self.tools_config[tool_name]
            if "version_command" in tool_info:
                result = subprocess.run(
                    tool_info["version_command"],
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                return result.stdout.strip()
            return None
        except Exception:
            return None

    def _get_last_update(self, tool_name: str) -> Optional[str]:
        """Get last update timestamp of tool"""
        try:
            tool_path = self.tools_dir / tool_name
            if tool_path.exists():
                timestamp = tool_path.stat().st_mtime
                return datetime.fromtimestamp(timestamp).isoformat()
            return None
        except Exception:
            return None

    def cleanup(self):
        """Cleanup tool manager resources"""
        try:
            # Stop all running processes
            for tool_name in list(self.active_processes.keys()):
                self.stop_tool(tool_name)

            self.logger.info("Tool manager resources cleaned up")

        except Exception as e:
            self.logger.error(f"Tool manager cleanup failed: {str(e)}")


class ToolManagerTab(QWidget):
    def __init__(self, tool_manager=None, parent=None):
        super().__init__(parent)
        self.tool_manager = tool_manager if tool_manager else ToolManager()
        self.init_ui()
        self.connect_signals()
        if tool_manager is None:
            self.refresh_tool_list()

    def init_ui(self):
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for tools...")
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Name", "Description", "Action"])
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.results_table)

        self.status_bar = QLabel()
        self.status_bar.setStyleSheet("color: #2196f3; font-weight: bold;")
        layout.addWidget(self.status_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(2)
        self.installed_table.setHorizontalHeaderLabels(["Tool Name", "Action"])
        header = self.installed_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.installed_table)

        self.setLayout(layout)

    def connect_signals(self):
        self.search_button.clicked.connect(self.search_tools)
        self.tool_manager.progress_signal.connect(self.update_progress)
        self.tool_manager.status_signal.connect(self.update_status)
        self.tool_manager.error_signal.connect(self.show_error)

    def search_tools(self):
        query = self.search_input.text()
        try:
            results = self.tool_manager.search_github(query)
            self.results_table.setRowCount(len(results))
            for row, tool in enumerate(results):
                name_item = QTableWidgetItem(tool["name"])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.results_table.setItem(row, 0, name_item)

                desc_item = QTableWidgetItem(tool.get("description", "No description"))
                desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.results_table.setItem(row, 1, desc_item)

                install_btn = QPushButton("Install")
                install_btn.clicked.connect(
                    lambda checked, t=tool: self.install_tool(t)
                )
                self.results_table.setCellWidget(row, 2, install_btn)
        except Exception as e:
            self.show_error(f"Search error: {str(e)}")

    def install_tool(self, tool):
        try:
            self.progress_bar.setVisible(True)
            result = self.tool_manager.download_tool(tool["html_url"])
            if result["status"] == "success":
                self.update_status(f"Installed: {result['tool_name']}")
                self.refresh_tool_list()
        except Exception as e:
            self.show_error(f"Installation error: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)

    def refresh_tool_list(self):
        tools = self.tool_manager.list_tools()
        self.installed_table.setRowCount(len(tools))
        for row, tool_name in enumerate(tools):
            name_item = QTableWidgetItem(tool_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.installed_table.setItem(row, 0, name_item)

            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, t=tool_name: self.remove_tool(t))
            self.installed_table.setCellWidget(row, 1, remove_btn)

    def remove_tool(self, tool_name):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {tool_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.tool_manager.delete_tool(tool_name)
                self.update_status(result)
                self.refresh_tool_list()
            except Exception as e:
                self.show_error(f"Error removing tool: {str(e)}")

    def update_progress(self, message, percentage):
        """
        Update the progress bar and status message.

        Parameters:
        message (str): The status message to display.
        percentage (int): The progress percentage to set on the progress bar.
        """
        self.update_status(f"{message} ({percentage}%)")
        self.progress_bar.setValue(percentage)

    def update_status(self, message):
        """
        Update the status bar with a given message to inform the user about the current status.

        Parameters:
        message (str): The message to display in the status bar.
        """
        self.status_bar.setText(message)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
