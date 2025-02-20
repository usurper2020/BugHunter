"""
Scanner tab interface for the BugHunter application.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from services.vulnerability_scanner import VulnerabilityScanner
from models.scan_target import ScanTarget

class ScannerTab(QWidget):
    """Tab widget for vulnerability scanning."""
    
    def __init__(self, scanner: VulnerabilityScanner):
        """Initialize the scanner interface."""
        super().__init__()
        self.scanner = scanner
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Target section
        target_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target URL")
        target_layout.addWidget(QLabel("Target:"))
        target_layout.addWidget(self.target_input)
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        target_layout.addWidget(self.scan_button)
        layout.addLayout(target_layout)
        
        # Results section
        layout.addWidget(QLabel("Scan Results:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)

    def start_scan(self):
        """Start vulnerability scan."""
        url = self.target_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL.")
            return
            
        # Create scan target
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        target = ScanTarget(url)
            
        # Start scan
        self.output_text.clear()
        self.output_text.append(f"Starting scan on {target.url}...")
        
        # Run the scan
        scan_result = self.scanner.run_scan(target)
        if scan_result['status'] == 'success':
            self.output_text.append("\nScan completed successfully!")
            self.output_text.append("\nFindings:")
            for finding in scan_result['results']['findings']:
                self.output_text.append(f"\n• {finding['type']} ({finding['severity']} severity)")
                self.output_text.append(f"  Description: {finding['description']}")
                self.output_text.append(f"  Details: {finding['details']}")
        else:
            self.output_text.append(f"\nScan failed: {scan_result['message']}")
