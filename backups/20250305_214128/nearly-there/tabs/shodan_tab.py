from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from typing import List
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
k = 10
query = ""
resources = []


"""
Shodan Integration Tab Module.

This module provides the Shodan integration interface for BugHunter,
allowing users to perform Shodan searches directly from the GUI.

    Classes:
    ShodanTab: Shodan integration tab class.
    """

   from PyQt6.QtWidgets import (
        QComboBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    from services.shodan_integration import ShodanIntegration

       class ShodanTab(QWidget):
        """
        Shodan integration tab for BugHunter.

            Attributes:
            search_input (QLineEdit): Input field for search queries.
            search_button (QPushButton): Button to initiate search.
            results_text (QTextEdit): Text area to display search results.
            filter_combo (QComboBox): Dropdown for search filters.
            """

           def __init__(self):
            """Initialize the Shodan tab."""
            super().__init__()
            self.shodan_client = ShodanIntegration()

            self.init_ui()
            self.connect_signals()

               def init_ui(self):
                """Initialize the user interface components."""
                layout = QVBoxLayout()

                # Search controls
                search_layout = QHBoxLayout()
                search_layout.add_widget(QLabel("Search Query:"))

                self.search_input = QLineEdit()
                self.search_input.set_placeholder_text(
                    "Enter search query")
                search_layout.add_widget(self.search_input)

                self.filter_combo = QComboBox()
                self.filter_combo.add_items(
                    ["All", "Host", "Port", "Vulnerability"])
                search_layout.add_widget(self.filter_combo)

                self.search_button = QPushButton("Search")
                search_layout.add_widget(self.search_button)

                layout.add_layout(search_layout)

                # Results display
                self.results_text = QTextEdit()
                self.results_text.set_read_only(True)
                layout.add_widget(self.results_text)

                self.set_layout(layout)

                   def connect_signals(self):
                    """Connect UI signals to appropriate slots."""
                    self.search_button.clicked.connect(self.perform_search)

                       def perform_search(self):
                        """Perform Shodan search and display results."""
                        query = self.search_input.text().strip()
                           if not query:
                            QMessageBox.warning(
                                self, "Invalid Input", "Please enter a search query")
                        return

                           try:
                            filter_type = self.filter_combo.current_text().lower()
                            results = self.shodan_client.search(
                                query, filter_type)
                            self.display_results(results)
                               except Exception as e:
                                QMessageBox.critical(
                                    self, "Search Error", f"Failed to perform search: {str(e)}"
                                )

                                   def display_results(self, _results):
                                    """Display search results in the text area.

                                            Args:
                                            results (list): List of search results to display.
                                            """
                                       self.results_text.clear()
                                           if not results:
                                            self.results_text.set_text(
                                                "No results found")
                                        return

                                        result_text = "\n\n".join(
                                            f"IP: {result.get('ip_str', 'N/A')}\n"
                                            f"Port: {result.get('port', 'N/A')}\n"
                                            f"Hostnames: {', '.join(result.get('hostnames', []))}\n"
                                            f"Vulnerabilities: {', '.join(result.get('vulns', []))}\n"
                                            f"Data: {result.get('data', 'N/A')[:200]}..."
                                            for result in results
                                        )
                                        self.results_text.set_text(
                                            result_text)

                                           def cleanup(self):
                                            """Clean up resources before closing."""
                                            self.results_text.clear()
