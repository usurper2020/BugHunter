"""Wayback tab implementation for the BugHunter application."""

from PyQt6.QtWidgets import (
    QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from services.wayback_machine_integration import WaybackMachineIntegration
from .base_tab import BaseTab
import logging

class WaybackTab(BaseTab):
    """Wayback Machine interface tab"""
    
    def __init__(self, wayback_integration: WaybackMachineIntegration, parent=None):
        self.wayback = wayback_integration
        self.logger = logging.getLogger('BugHunter.WaybackTab')
        super().__init__(parent)
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Create search section
        search_group = QGroupBox("Wayback Search")
        search_layout = QVBoxLayout()
        search_group.setLayout(search_layout)
        
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to search...")
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._perform_search)
        
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.search_button)
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems([
            "Snapshots",
            "Page Changes",
            "Content Analysis"
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
        
        self._update_status("Wayback integration ready.")
    
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
        """Handle Wayback search"""
        url = self.url_input.text().strip()
        if not url:
            self._update_status("Please enter a URL")
            return
        
        search_type = self.search_type_combo.currentText()
        try:
            self._update_status(f"Performing {search_type}...")
            if search_type == "Snapshots":
                results = self.wayback.get_snapshots(url)
            elif search_type == "Page Changes":
                results = self.wayback.get_page_changes(url)
            else:  # Content Analysis
                results = self.wayback.analyze_content(url)
            
            self._display_results(results)
            self._update_status(f"{search_type} completed successfully")
        except Exception as e:
            self._update_status(f"Error performing search: {str(e)}")
            self.logger.error(f"Error performing search: {str(e)}")
    
    def refresh(self):
        """Refresh tab content"""
        self.url_input.clear()
        self.results_display.clear()
        self._update_status("Wayback tab refreshed.")
