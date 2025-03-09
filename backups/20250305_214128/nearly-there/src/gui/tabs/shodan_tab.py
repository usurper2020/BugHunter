from .base_tab import BaseTab
from services.shodan_integration import ShodanIntegration
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
value = None
key = ""
k = 10
query = ""
content = ""
message = ""
items = []


"""Shodan tab implementation for the BugHunter application."""


class ShodanTab(BaseTab):
    """Shodan interface tab"""

    def __init__(self, _shodan_integration: ShodanIntegration, _parent=None):
        self.shodan = shodan_integration
        self.logger = logging.get_logger("BugHunter.ShodanTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create search section
            search_group = QGroupBox("Shodan Search")
            search_layout = QVBoxLayout()
            search_group.set_layout(search_layout)

            input_layout = QHBoxLayout()
            self.search_input = QLineEdit()
            self.search_input.set_placeholder_text("Enter search query...")

            self.search_button = QPushButton("Search")
            self.search_button.clicked.connect(self._perform_search)

            input_layout.add_widget(self.search_input)
            input_layout.add_widget(self.search_button)

            self.search_type_combo = QComboBox()
            self.search_type_combo.add_items(
                ["Host Search", "Exploit Search", "Service Search"]
            )

            search_layout.add_layout(input_layout)
            search_layout.add_widget(self.search_type_combo)

            # Create results section
            results_group = QGroupBox("Search Results")
            results_layout = QVBoxLayout()
            results_group.set_layout(results_layout)

            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            self.results_display.set_placeholder_text(
                "Search results will appear here...")
            results_layout.add_widget(self.results_display)

            # Add status section
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.set_layout(status_layout)

            self.status_label = QLabel("Ready")
            status_layout.add_widget(self.status_label)

            # Add all components to main layout
            self.layout.add_widget(search_group)
            self.layout.add_widget(results_group)
            self.layout.add_widget(status_group)

            self._update_status("Shodan integration ready.")

            def _update_status(self, _message: str):
                """Update status message"""
                self.status_label.set_text(message)
                self.logger.info(message)

                def _display_results(self, _results):
                    """Display search results"""
                    self.results_display.clear()
                    if isinstance(results, dict):
                        for key, value in results.items():
                            self.results_display.append(
                                f"<b>{key}:</b> {value}")
                            else:
                                self.results_display.append(str(results))

                                @pyqt_slot()
                                def _perform_search(self):
                                    """Handle Shodan search"""
                                    query = self.search_input.text().strip()
                                    if not query:
                                        self._update_status(
                                            "Please enter a search query")
                                    return

                                    search_type = self.search_type_combo.current_text()
                                    try:
                                        self._update_status(
                                            f"Performing {search_type}...")
                                        if search_type == "Host Search":
                                            results = self.shodan.host_search(
                                                query)
                                            elif search_type == "Exploit Search":
                                                results = self.shodan.exploit_search(
                                                    query)
                                                else:  # Service Search
                                                results = self.shodan.service_search(
                                                    query)

                                                self._display_results(results)
                                                self._update_status(
                                                    f"{search_type} completed successfully")
                                                except Exception as e:
                                                    self._update_status(
                                                        f"Error performing search: {str(e)}")
                                                    self.logger.error(
                                                        f"Error performing search: {str(e)}")

                                                    def refresh(self):
                                                        """Refresh tab content"""
                                                        self.search_input.clear()
                                                        self.results_display.clear()
                                                        self._update_status(
                                                            "Shodan tab refreshed.")
