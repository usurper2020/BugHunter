from services.vulnerability_scanner import VulnerabilityScanner
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

k = 10
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
        self.scanner = VulnerabilityScanner()  # Initialize scanner first
        self.init_ui()

        def init_ui(self):
            """Initialize the UI components."""
            layout = QVBoxLayout()

            # Scan profile selection
            self.profile_selector = QComboBox()
            self.profile_selector.add_items(self.scanner.get_profiles())
            layout.add_widget(QLabel("Select Scan Profile:"))
            layout.add_widget(self.profile_selector)

            # Target input
            self.target_input = QTextEdit()
            self.target_input.set_placeholder_text(
                "Enter target URLs (one per line)")
            layout.add_widget(self.target_input)

            # Scan button
            scan_button = QPushButton("Run Scan")
            scan_button.clicked.connect(self.run_scan)
            layout.add_widget(scan_button)

            # Results display
            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            layout.add_widget(QLabel("Scan Results:"))
            layout.add_widget(self.results_display)

            self.set_layout(layout)

            def run_scan(self):
                """Run a security scan on the specified targets."""
                profile = self.profile_selector.current_text()
                targets = self.target_input.to_plain_text().strip().split("\n")
                if targets:
                    results = self.scanner.scan(targets, profile)
                    self.results_display.set_plain_text(results)
