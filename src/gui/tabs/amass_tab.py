"""Amass tab implementation for the BugHunter application."""

from PyQt6.QtWidgets import (
    QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QGroupBox, QComboBox, QProgressBar
)

from PyQt6.QtCore import Qt, pyqtSlot
from services.tool_manager import ToolManager
from .base_tab import BaseTab
import logging

class AmassTab(BaseTab):
    """Amass interface tab"""
    
    def __init__(self, tool_manager: ToolManager, parent=None):
        self.tool_manager = tool_manager
        self.logger = logging.getLogger('BugHunter.AmassTab')
        super().__init__(parent)
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Create scan section
        scan_group = QGroupBox("Amass Scan")
        scan_layout = QVBoxLayout()
        scan_group.setLayout(scan_layout)
        
        input_layout = QHBoxLayout()
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter target domain...")
        
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self._start_scan)
        
        input_layout.addWidget(self.domain_input)
        input_layout.addWidget(self.scan_button)
        
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems([
            "Passive Scan",
            "Active Scan",
            "Full Enumeration"
        ])
        
        scan_layout.addLayout(input_layout)
        scan_layout.addWidget(self.scan_type_combo)
        
        # Create results section
        results_group = QGroupBox("Scan Results")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText("Scan results will appear here...")
        results_layout.addWidget(self.results_display)
        
        # Add status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        # Add all components to main layout
        self.layout.addWidget(scan_group)
        self.layout.addWidget(results_group)
        self.layout.addWidget(status_group)
        
        self._update_status("Amass scanner ready.")
    
    def _update_status(self, message: str):
        """Update status message"""
        self.status_label.setText(message)
        self.logger.info(message)
    
    def _update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def _display_results(self, results):
        """Display scan results"""
        self.results_display.clear()
        if isinstance(results, dict):
            for key, value in results.items():
                self.results_display.append(f"<b>{key}:</b> {value}")
        else:
            self.results_display.append(str(results))
    
    @pyqtSlot()
    def _start_scan(self):
        """Handle Amass scan"""
        domain = self.domain_input.text().strip()
        if not domain:
            self._update_status("Please enter a domain")
            return
        
        scan_type = self.scan_type_combo.currentText()
        try:
            self._update_status(f"Starting {scan_type}...")
            self._update_progress(0)
            
            # Start the scan
            amass = self.tool_manager.get_tool('amass')
            results = amass.run_scan(domain, scan_type.lower())
            
            # Update UI with results
            self._display_results(results)
            self._update_progress(100)
            self._update_status(f"{scan_type} completed successfully")
        except Exception as e:
            self._update_status(f"Error during scan: {str(e)}")
            self.logger.error(f"Error during scan: {str(e)}")
            self._update_progress(0)
    
    def refresh(self):
        """Refresh tab content"""
        self.domain_input.clear()
        self.results_display.clear()
        self._update_progress(0)
        self._update_status("Amass tab refreshed.")
