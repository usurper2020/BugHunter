
"""
Scanner Tab Module

This module implements the ScannerTab class, which provides the user interface
for executing security scans within the BugHunter application. The tab allows
users to:

- Select from predefined scan profiles
- Input target URLs or IP addresses
- Execute scans with selected profiles
- View detailed scan results

The tab integrates with the VulnerabilityScanner service to perform actual
scan operations and display results in real-time.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit
from services.vulnerability_scanner import VulnerabilityScanner

class ScannerTab(QWidget):
    """Provides a comprehensive interface for security scanning operations.
    
    The ScannerTab widget offers a complete workflow for vulnerability scanning,
    including target selection, profile configuration, scan execution, and
    results visualization. It serves as the primary interface for users to
    interact with the BugHunter scanning capabilities.
    
    Attributes:
        profile_selector (QComboBox): Dropdown for selecting scan profiles
        target_input (QTextEdit): Field for entering scan targets
        results_display (QTextEdit): Area for displaying scan results
        scanner (VulnerabilityScanner): Service for executing scans
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanner = VulnerabilityScanner()

    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Scan profile selection
        self.profile_selector = QComboBox()
        self.profile_selector.addItems(self.scanner.get_profiles())
        layout.addWidget(QLabel("Select Scan Profile:"))
        layout.addWidget(self.profile_selector)
        
        # Target input
        self.target_input = QTextEdit()
        self.target_input.setPlaceholderText("Enter target URLs (one per line)")
        layout.addWidget(self.target_input)
        
        # Scan button
        scan_button = QPushButton("Run Scan")
        scan_button.clicked.connect(self.run_scan)
        layout.addWidget(scan_button)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(QLabel("Scan Results:"))
        layout.addWidget(self.results_display)
        
        self.setLayout(layout)

    def run_scan(self):
        """Run a security scan on the specified targets."""
        profile = self.profile_selector.currentText()
        targets = self.target_input.toPlainText().strip().split('\n')
        if targets:
            results = self.scanner.scan(targets, profile)
            self.results_display.setPlainText(results)
