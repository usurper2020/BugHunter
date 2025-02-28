"""Shodan tab implementation for the BugHunter application."""

from PyQt6.QtWidgets import (
    QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from services.shodan_integration import ShodanIntegration
from .base_tab import BaseTab
import logging

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
