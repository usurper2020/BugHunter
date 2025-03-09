from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
k = 10
resources = []
"""
Shodan Integration Tab Module.

This module provides the Shodan integration interface for BugHunter,
allowing users to perform security reconnaissance directly from the GUI.

    Classes:
    ShodanTab: Shodan integration tab class.
    """

   from PyQt6.QtWidgets import (
        QCheckBox,
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
            target_input (QLineEdit): Input field for target to search.
            search_button (QPushButton): Button to initiate search.
            results_text (QTextEdit): Text area to display search results.
            filter_combo (QComboBox): Dropdown for search filters.
            real_time_checkbox (QCheckBox): Checkbox to enable real-time monitoring.
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
                search_layout.add_widget(QLabel("Target:"))

                self.target_input = QLineEdit()
                self.target_input.set_placeholder_text(
                    "Enter target to search (IP, domain, etc.)"
                )
                search_layout.add_widget(self.target_input)

                self.filter_combo = QComboBox()
                self.filter_combo.add_items(
                    ["All", "Open Ports", "Services", "Organizations"])
                search_layout.add_widget(self.filter_combo)

                self.search_button = QPushButton("Search")
                search_layout.add_widget(self.search_button)

                layout.add_layout(search_layout)

                # Real-time monitoring checkbox
                self.real_time_checkbox = QCheckBox(
                    "Enable Real-time Monitoring")
                layout.add_widget(self.real_time_checkbox)

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
                        target = self.target_input.text().strip()
                           if not target:
                            QMessageBox.warning(
                                self, "Invalid Input", "Please enter a target")
                        return

                           try:
                            filter_option = self.filter_combo.current_text()
                            results = self.shodan_client.search(
                                target, filter_option)
                            self.display_results(results)
                               except Exception as e:
                                QMessageBox.critical(
                                    self, "Search Error", f"Failed to perform search: {str(e)}"
                                )

                                   def display_results(self, results):
                                    """Display search results in the text area.

                                            Args:
                                            results (dict): Dictionary of search results to display.
                                            """
                                       self.results_text.clear()
                                           if not results.get("results"):
                                            self.results_text.set_text(
                                                "No results found")
                                        return

                                        result_text = "\n\n".join(
                                            f"IP: {result.get('ip_str', 'N/A')}\n"
                                            f"Port: {result.get('port', 'N/A')}\n"
                                            f"Data: {result.get('data', 'N/A')}\n"
                                            f"Geolocation: {result.get('location', {}).get('city', 'N/A')}, {result.get('location', {}).get('country_name', 'N/A')}\n"
                                            f"Vulnerabilities: {', '.join(result.get('vulns', []))}"
                                            for result in results["results"]
                                        )
                                        self.results_text.set_text(
                                            result_text)

                                           if self.real_time_checkbox.is_checked():
                                                # Display real-time monitoring status (this is a placeholder, actual
                                                # implementation may vary)
                                            self.results_text.append(
                                                "\n[Real-time Monitoring Enabled]")

                                               def cleanup(self):
                                                """Clean up resources before closing."""
                                                self.results_text.clear()
