"""Shodan tab implementation for the BugHunter application."""

from PyQt6.QtWidgets import (
    QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from services.shodan_integration import ShodanIntegration
from .base_tab import BaseTab
import logging


class ShodanTab(QWidget):
    def __init__(self):
        super().__init__()
        self.shodan_client = ShodanClient()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Query:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query")
        search_layout.addWidget(self.search_input)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Host", "Port", "Vulnerability"])
        search_layout.addWidget(self.filter_combo)
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        self.setLayout(layout)

    def connect_signals(self):
        self.search_button.clicked.connect(self.perform_search)

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Invalid Input", "Please enter a search query")
            return
        try:
            filter_type = self.filter_combo.currentText().lower()
            results = self.shodan_client.search(query, filter_type)
            self.display_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"Failed to perform search: {str(e)}")

    def display_results(self, results):
        self.results_text.clear()
        if not results:
            self.results_text.setText("No results found")
            return
        result_text = "\n\n".join(
            f"IP: {result.get('ip_str', 'N/A')}\n"
            f"Port: {result.get('port', 'N/A')}\n"
            f"Hostnames: {', '.join(result.get('hostnames', []))}\n"
            f"Vulnerabilities: {', '.join(result.get('vulns', []))}\n"
            f"Data: {result.get('data', 'N/A')[:200]}..."
            for result in results
        )
        self.results_text.setText(result_text)

    def cleanup(self):
        self.results_text.clear()



class ShodanTab(BaseTab):
    """Shodan interface tab"""
    
    def __init__(self, shodan_integration: ShodanIntegration, parent=None):
        self.shodan = shodan_integration
        self.logger = logging.getLogger('BugHunter.ShodanTab')
        super().__init__(parent)
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Create search section
        search_group = QGroupBox("Shodan Search")
        search_layout = QVBoxLayout()
        search_group.setLayout(search_layout)
        
        input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query...")
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._perform_search)
        
        input_layout.addWidget(self.search_input)
        input_layout.addWidget(self.search_button)
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems([
            "Host Search",
            "Exploit Search",
            "Service Search"
        ])
        
        search_layout.addLayout(input_layout)
        search_layout.addWidget(self.search_type_combo)
        
        # Create results section
        results_group = QGroupBox("Search Results")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText("Search results will appear here...")
        results_layout.addWidget(self.results_display)
        
        # Add status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        
        # Add all components to main layout
        self.layout.addWidget(search_group)
        self.layout.addWidget(results_group)
        self.layout.addWidget(status_group)
        
        self._update_status("Shodan integration ready.")
    
    def _update_status(self, message: str):
        """Update status message"""
        self.status_label.setText(message)
        self.logger.info(message)
    
    def _display_results(self, results):
        """Display search results"""
        self.results_display.clear()
        if isinstance(results, dict):
            for key, value in results.items():
                self.results_display.append(f"<b>{key}:</b> {value}")
        else:
            self.results_display.append(str(results))
    
    @pyqtSlot()
    def _perform_search(self):
        """Handle Shodan search"""
        query = self.search_input.text().strip()
        if not query:
            self._update_status("Please enter a search query")
            return
        
        search_type = self.search_type_combo.currentText()
        try:
            self._update_status(f"Performing {search_type}...")
            if search_type == "Host Search":
                results = self.shodan.host_search(query)
            elif search_type == "Exploit Search":
                results = self.shodan.exploit_search(query)
            else:  # Service Search
                results = self.shodan.service_search(query)
            
            self._display_results(results)
            self._update_status(f"{search_type} completed successfully")
        except Exception as e:
            self._update_status(f"Error performing search: {str(e)}")
            self.logger.error(f"Error performing search: {str(e)}")
    
    def refresh(self):
        """Refresh tab content"""
        self.search_input.clear()
        self.results_display.clear()
        self._update_status("Shodan tab refreshed.")
