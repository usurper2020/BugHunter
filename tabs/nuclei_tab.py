"""
Nuclei tab for the BugHunter application.

This tab provides an interface for running Nuclei scans
and managing Nuclei templates.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from services.nuclei_analyzer import NucleiAnalyzer

class NucleiTab(QWidget):
    """
    Tab widget for Nuclei scanning functionality.
    
    This widget provides:
    - Input field for target URLs
    - Button to run Nuclei scans
    - Output display for scan results
    - Template management
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.analyzer = NucleiAnalyzer()

    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Target input
        self.target_input = QTextEdit()
        self.target_input.setPlaceholderText("Enter target URLs (one per line)")
        layout.addWidget(self.target_input)
        
        # Scan button
        scan_button = QPushButton("Run Nuclei Scan")
        scan_button.clicked.connect(self.run_scan)
        layout.addWidget(scan_button)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(QLabel("Scan Results:"))
        layout.addWidget(self.results_display)
        
        self.setLayout(layout)

    def run_scan(self):
        """Run a Nuclei scan on the specified targets."""
        targets = self.target_input.toPlainText().strip().split('\n')
        if targets:
            results = self.analyzer.scan(targets)
            self.results_display.setPlainText(results)
