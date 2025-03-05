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
    QMessageBox, QDateEdit, QCheckBox, QSplitter, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal, QDate
from services.wayback_machine_integration import WaybackMachineIntegration


class WaybackTab(QWidget):
    """
    Wayback Machine integration tab for BugHunter.

    Attributes:
        url_input (QLineEdit): Input field for URL to search.
        search_button (QPushButton): Button to initiate search.
        results_table (QTableWidget): Table to display search results.
        date_combo (QComboBox): Dropdown for date filters.
        start_date_edit (QDateEdit): Date edit for start date.
        end_date_edit (QDateEdit): Date edit for end date.
        preview_checkbox (QCheckBox): Checkbox to enable snapshot preview.
        compare_button (QPushButton): Button to compare two snapshots.
        bookmark_button (QPushButton): Button to bookmark a snapshot.
        export_button (QPushButton): Button to export search results.
    """

    def __init__(self):
        """Initialize the Wayback tab."""
        super().__init__()
        self.wayback_client = WaybackMachineIntegration()

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
        self.date_combo.addItems(["All", "Last Year", "Last 5 Years", "Specific Date Range"])
        search_layout.addWidget(self.date_combo)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addYears(-5))
        search_layout.addWidget(self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        search_layout.addWidget(self.end_date_edit)
        
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)

        # Preview checkbox
        self.preview_checkbox = QCheckBox("Enable Snapshot Preview")
        layout.addWidget(self.preview_checkbox)

        # Compare button
        self.compare_button = QPushButton("Compare Snapshots")
        layout.addWidget(self.compare_button)

        # Bookmark button
        self.bookmark_button = QPushButton("Bookmark Snapshot")
        layout.addWidget(self.bookmark_button)

        # Export button
        self.export_button = QPushButton("Export Results")
        layout.addWidget(self.export_button)

        # Results display
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Date", "URL", "Status", "Snapshot"])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def connect_signals(self):
        """Connect UI signals to appropriate slots."""
        self.search_button.clicked.connect(self.perform_search)
        self.compare_button.clicked.connect(self.compare_snapshots)
        self.bookmark_button.clicked.connect(self.bookmark_snapshot)
        self.export_button.clicked.connect(self.export_results)

    def perform_search(self):
        """Perform Wayback Machine search and display results."""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Invalid Input", "Please enter a URL")
            return

        try:
            date_filter = self.date_combo.currentText()
            if date_filter == "Specific Date Range":
                start_date = self.start_date_edit.date().toString("yyyyMMdd")
                end_date = self.end_date_edit.date().toString("yyyyMMdd")
                results = self.wayback_client.get_snapshots_in_range(url, start_date, end_date)
            else:
                results = self.wayback_client.search_url(url, date_filter)
            self.display_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"Failed to perform search: {str(e)}")

    def display_results(self, results):
        """Display search results in the table.
        
        Args:
            results (list): List of search results to display.
        """
        self.results_table.setRowCount(0)
        if not results:
            QMessageBox.information(self, "No Results", "No results found")
            return

        for result in results:
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            self.results_table.setItem(row_position, 0, QTableWidgetItem(result.get('timestamp', 'N/A')))
            self.results_table.setItem(row_position, 1, QTableWidgetItem(result.get('url', 'N/A')))
            self.results_table.setItem(row_position, 2, QTableWidgetItem(result.get('status', 'N/A')))
            self.results_table.setItem(row_position, 3, QTableWidgetItem(result.get('snapshot_url', 'N/A')))

        if self.preview_checkbox.isChecked():
            # Display snapshot preview (this is a placeholder, actual implementation may vary)
            QMessageBox.information(self, "Snapshot Preview", "Snapshot preview feature is enabled.")

    def compare_snapshots(self):
        """Compare two snapshots side-by-side."""
        # Placeholder for snapshot comparison logic
        QMessageBox.information(self, "Compare Snapshots", "Snapshot comparison feature is under development.")

    def bookmark_snapshot(self):
        """Bookmark a selected snapshot."""
        # Placeholder for bookmarking logic
        QMessageBox.information(self, "Bookmark Snapshot", "Bookmarking feature is under development.")

    def export_results(self):
        """Export search results to a file."""
        # Placeholder for export logic
        QMessageBox.information(self, "Export Results", "Export feature is under development.")

    def cleanup(self):
        """Clean up resources before closing."""
        self.results_table.setRowCount(0)
