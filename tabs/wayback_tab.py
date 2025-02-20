"""
Wayback Machine Integration Tab Module.

This module provides the Wayback Machine integration interface for BugHunter,
allowing users to access archived web pages directly from the GUI.

Classes:
    WaybackTab: Wayback Machine integration tab class.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QComboBox,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from services.wayback_machine_integration import WaybackClient

class WaybackTab(QWidget):
    """
    Wayback Machine integration tab for BugHunter.

    Attributes:
        url_input (QLineEdit): Input field for URL to search.
        search_button (QPushButton): Button to initiate search.
        results_text (QTextEdit): Text area to display search results.
        date_combo (QComboBox): Dropdown for date filters.
    """

    def __init__(self):
        """Initialize the Wayback tab."""
        super().__init__()
        self.wayback_client = WaybackClient()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout()

        # Search controls
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("URL:"))
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to search")
        search_layout.addWidget(self.url_input)
        
        self.date_combo = QComboBox()
        self.date_combo.addItems(["All", "Last Year", "Last 5 Years", "Specific Date"])
        search_layout.addWidget(self.date_combo)
        
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)

        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)

    def connect_signals(self):
        """Connect UI signals to appropriate slots."""
        self.search_button.clicked.connect(self.perform_search)

    def perform_search(self):
        """Perform Wayback Machine search and display results."""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Invalid Input", "Please enter a URL")
            return

        try:
            date_filter = self.date_combo.currentText()
            results = self.wayback_client.search(url, date_filter)
            self.display_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"Failed to perform search: {str(e)}")

    def display_results(self, results):
        """Display search results in the text area.
        
        Args:
            results (list): List of search results to display.
        """
        self.results_text.clear()
        if not results:
            self.results_text.setText("No results found")
            return

        result_text = "\n\n".join(
            f"Date: {result.get('timestamp', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Status: {result.get('status', 'N/A')}\n"
            f"Snapshot: {result.get('snapshot_url', 'N/A')}"
            for result in results
        )
        self.results_text.setText(result_text)

    def cleanup(self):
        """Clean up resources before closing."""
        self.results_text.clear()
