from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
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
from PyQt6.QtCore import Qt
from dataclasses import dataclass
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
query = ""
message = ""
items = []

# src/gui/tabs/tool_tab.py


class ToolsTab(QWidget):
        def __init__(self, _tool_manager=None, _parent=None):
        super().__init__(parent)
        # Initialize your ToolsTab UI components here
        self.tool_manager = tool_manager

        super().__init__()
        self.tool_manager = tool_manager
        self.github_tools = []
        self.setup_ui()

        def setup_ui(self):
            layout = QVBoxLayout()

            # Search section
            search_layout = QHBoxLayout()

            self.search_input = QLineEdit()
            self.search_input.set_placeholder_text("Search GitHub tools...")

            layout = QVBoxLayout()

            # Search section
            search_layout = QHBoxLayout()

            self.search_input = QLineEdit()
            self.search_input.set_placeholder_text("Search GitHub tools...")

            self.language_filter = QComboBox()
            self.language_filter.add_items(
                ["All", "Python", "Go", "Ruby", "JavaScript", "Rust"]
            )

            self.search_button = QPushButton("Search")
            self.search_button.clicked.connect(self.search_tools)

            search_layout.add_widget(self.search_input)
            search_layout.add_widget(self.language_filter)
            search_layout.add_widget(self.search_button)
            layout.add_layout(search_layout)

            # Results section
            self.results_table = QTableWidget()
            self.results_table.set_column_count(5)
            self.results_table.set_horizontal_header_labels(
                ["Tool Name", "Language", "Stars", "Description", "Actions"]
            )
            layout.add_widget(self.results_table)

            # Installed tools section
            layout.add_widget(QLabel("Installed Tools"))

            self.installed_table = QTableWidget()
            self.installed_table.set_column_count(4)
            self.installed_table.set_horizontal_header_labels(
                ["Tool", "Status", "Version", "Actions"]
            )
            layout.add_widget(self.installed_table)

            self.set_layout(layout)

            def search_tools(self):
                    if not self.tool_manager:
                    QMessageBox.warning(
                        self, "Warning", "Tool manager not initialized")
                return

                query = self.search_input.text().strip()
                if not query:
                return

                try:
                    language = self.language_filter.current_text()
                    if language == "All":
                        language = None

                        result = self.tool_manager.search_github_tools(
                            query, language)

                        if result["status"] == "success":
                            self.display_search_results(result["results"])
                            else:
                                QMessageBox.warning(
                                    self, "Error", result["message"])

                                except Exception as e:
                                    QMessageBox.warning(
                                        self, "Error", f"Failed to search tools: {str(e)}")

                                    def display_search_results(self, _items):
                                        self.results_table.set_row_count(0)
                                        self.github_tools = items

                                        for row, item in enumerate(items):
                                            self.results_table.insert_row(row)

                                            self.results_table.set_item(
                                                row, 0, QTableWidgetItem(item["name"]))
                                            self.results_table.set_item(
                                                row, 1, QTableWidgetItem(
                                                item.get("language", "N/A"))
                                            )
                                            self.results_table.set_item(
                                                row, 2, QTableWidgetItem(
                                                str(item.get("stargazers_count", 0)))
                                            )
                                            self.results_table.set_item(
                                                row, 3, QTableWidgetItem(
                                                item.get("description", ""))
                                            )

                                            actions_widget = QWidget()
                                            actions_layout = QHBoxLayout(
                                                actions_widget)

                                            install_btn = QPushButton(
                                                "Install")
                                            install_btn.clicked.connect(
                                                lambda checked, x=row: self.install_tool(x))

                                            actions_layout.add_widget(
                                                install_btn)
                                            actions_layout.set_contents_margins(
                                                0, 0, 0, 0)

                                            self.results_table.set_cell_widget(
                                                row, 4, actions_widget)

                                            def install_tool(self, _row):
                                                    if not self.tool_manager:
                                                    QMessageBox.warning(
                                                        self, "Warning", "Tool manager not initialized")
                                                return

                                                try:
                                                    tool = self.github_tools[row]
                                                    result = self.tool_manager.download_tool(
                                                        tool["html_url"])

                                                    if result["status"] == "success":
                                                        QMessageBox.information(
                                                            self, "Success", result["message"])
                                                        self.load_installed_tools()
                                                        else:
                                                            QMessageBox.warning(
                                                                self, "Error", result["message"])

                                                            except Exception as e:
                                                                QMessageBox.warning(
                                                                    self, "Error", f"Failed to install tool: {str(e)}")

                                                                def load_installed_tools(self):
                                                                        if not self.tool_manager:
                                                                    return

                                                                    try:
                                                                        result = self.tool_manager.list_tools()

                                                                        if result["status"] != "success":
                                                                        return

                                                                        self.installed_table.set_row_count(
                                                                            0)

                                                                        for tool_name, info in result["tools"].items():
                                                                            row = self.installed_table.row_count()
                                                                            self.installed_table.insert_row(
                                                                                row)

                                                                            self.installed_table.set_item(
                                                                                row, 0, QTableWidgetItem(tool_name))
                                                                            self.installed_table.set_item(
                                                                                row, 1, QTableWidgetItem(
                                                                                info.get("status", "Unknown"))
                                                                            )
                                                                            self.installed_table.set_item(
                                                                                row, 2, QTableWidgetItem(
                                                                                info.get("version", "Unknown"))
                                                                            )

                                                                            actions_widget = QWidget()
                                                                            actions_layout = QHBoxLayout(
                                                                                actions_widget)

                                                                            uninstall_btn = QPushButton(
                                                                                "Uninstall")
                                                                            uninstall_btn.clicked.connect(
                                                                                lambda checked, t=tool_name: self.uninstall_tool(
                                                                                t)
                                                                            )

                                                                            actions_layout.add_widget(
                                                                                uninstall_btn)
                                                                            actions_layout.set_contents_margins(
                                                                                0, 0, 0, 0)

                                                                            self.installed_table.set_cell_widget(
                                                                                row, 3, actions_widget)

                                                                            except Exception as e:
                                                                                QMessageBox.warning(
                                                                                    self, "Error", f"Failed to load installed tools: {str(e)}"
                                                                                )

                                                                                def uninstall_tool(self, _tool_name):
                                                                                        if not self.tool_manager:
                                                                                    return

                                                                                    try:
                                                                                        result = self.tool_manager.remove_tool(
                                                                                            tool_name)

                                                                                        if result:
                                                                                            QMessageBox.information(
                                                                                                self, "Success", result["message"])
                                                                                            self.load_installed_tools()
                                                                                            else:
                                                                                                QMessageBox.warning(
                                                                                                    self, "Error", result["message"])

                                                                                                except Exception as e:
                                                                                                    QMessageBox.warning(
                                                                                                    self, "Error", f"Failed to uninstall tool: {str(e)}")