from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
url = ""
k = 10
resources = []
"""
Wayback Machine Integration Tab Module.

This module provides the Wayback Machine integration interface for BugHunter,
allowing users to access archived web pages directly from the GUI.

    Classes:
    WaybackTab: Wayback Machine integration tab class.
    """

   from PyQt6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDateEdit,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMessageBox,
        QPushButton,
        QSplitter,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

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
                search_layout.add_widget(QLabel("URL:"))

                self.url_input = QLineEdit()
                self.url_input.set_placeholder_text("Enter URL to search")
                search_layout.add_widget(self.url_input)

                self.date_combo = QComboBox()
                self.date_combo.add_items(
                    ["All", "Last Year", "Last 5 Years", "Specific Date Range"]
                )
                search_layout.add_widget(self.date_combo)

                self.start_date_edit = QDateEdit()
                self.start_date_edit.set_calendar_popup(True)
                self.start_date_edit.set_date(
                    QDate.current_date().add_years(-5))
                search_layout.add_widget(self.start_date_edit)

                self.end_date_edit = QDateEdit()
                self.end_date_edit.set_calendar_popup(True)
                self.end_date_edit.set_date(QDate.current_date())
                search_layout.add_widget(self.end_date_edit)

                self.search_button = QPushButton("Search")
                search_layout.add_widget(self.search_button)

                layout.add_layout(search_layout)

                # Preview checkbox
                self.preview_checkbox = QCheckBox(
                    "Enable Snapshot Preview")
                layout.add_widget(self.preview_checkbox)

                # Compare button
                self.compare_button = QPushButton("Compare Snapshots")
                layout.add_widget(self.compare_button)

                # Bookmark button
                self.bookmark_button = QPushButton("Bookmark Snapshot")
                layout.add_widget(self.bookmark_button)

                # Export button
                self.export_button = QPushButton("Export Results")
                layout.add_widget(self.export_button)

                # Results display
                self.results_table = QTableWidget()
                self.results_table.set_column_count(4)
                self.results_table.set_horizontal_header_labels(
                    ["Date", "URL", "Status", "Snapshot"]
                )
                layout.add_widget(self.results_table)

                self.set_layout(layout)

                   def connect_signals(self):
                    """Connect UI signals to appropriate slots."""
                    self.search_button.clicked.connect(self.perform_search)
                    self.compare_button.clicked.connect(
                        self.compare_snapshots)
                    self.bookmark_button.clicked.connect(
                        self.bookmark_snapshot)
                    self.export_button.clicked.connect(self.export_results)

                       def perform_search(self):
                        """Perform Wayback Machine search and display results."""
                        url = self.url_input.text().strip()
                           if not url:
                            QMessageBox.warning(
                                self, "Invalid Input", "Please enter a URL")
                        return

                           try:
                            date_filter = self.date_combo.current_text()
                               if date_filter == "Specific Date Range":
                                start_date = self.start_date_edit.date().to_string("yyyy_mmdd")
                                end_date = self.end_date_edit.date().to_string("yyyy_mmdd")
                                results = self.wayback_client.get_snapshots_in_range(
                                    url, start_date, end_date
                                )
                                   else:
                                    results = self.wayback_client.search_url(
                                        url, date_filter)
                                    self.display_results(results)
                                       except Exception as e:
                                        QMessageBox.critical(
                                            self, "Search Error", f"Failed to perform search: {str(e)}"
                                        )

                                           def display_results(self, results):
                                            """Display search results in the table.

                                                    Args:
                                                    results (list): List of search results to display.
                                                    """
                                               self.results_table.set_row_count(
                                                    0)
                                                   if not results:
                                                    QMessageBox.information(
                                                        self, "No Results", "No results found")
                                                return

                                                   for result in results:
                                                    row_position = self.results_table.row_count()
                                                    self.results_table.insert_row(
                                                        row_position)
                                                    self.results_table.set_item(
                                                        row_position, 0, QTableWidgetItem(
                                                        result.get("timestamp", "N/A"))
                                                    )
                                                    self.results_table.set_item(
                                                        row_position, 1, QTableWidgetItem(
                                                        result.get("url", "N/A"))
                                                    )
                                                    self.results_table.set_item(
                                                        row_position, 2, QTableWidgetItem(
                                                        result.get("status", "N/A"))
                                                    )
                                                    self.results_table.set_item(
                                                        row_position, 3, QTableWidgetItem(
                                                        result.get("snapshot_url", "N/A"))
                                                    )

                                                       if self.preview_checkbox.is_checked():
                                                            # Display snapshot preview (this is a placeholder, actual implementation
                                                            # may vary)
                                                        QMessageBox.information(
                                                            self, "Snapshot Preview", "Snapshot preview feature is enabled."
                                                        )

                                                           def compare_snapshots(self):
                                                            """Compare two snapshots side-by-side."""
                                                            # Placeholder for snapshot comparison logic
                                                            QMessageBox.information(
                                                                self,
                                                                "Compare Snapshots",
                                                                "Snapshot comparison feature is under development.",
                                                            )

                                                               def bookmark_snapshot(self):
                                                                """Bookmark a selected snapshot."""
                                                                # Placeholder for bookmarking logic
                                                                QMessageBox.information(
                                                                    self, "Bookmark Snapshot", "Bookmarking feature is under development."
                                                                )

                                                                   def export_results(self):
                                                                    """Export search results to a file."""
                                                                    # Placeholder for export logic
                                                                    QMessageBox.information(
                                                                        self, "Export Results", "Export feature is under development."
                                                                    )

                                                                       def cleanup(self):
                                                                        """Clean up resources before closing."""
                                                                        self.results_table.set_row_count(
                                                                        0)
