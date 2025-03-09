from .base_tab import BaseTab
from services.vulnerability_scanner import VulnerabilityScanner
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
value = None
key = ""
k = 10
content = ""
message = ""
items = []


"""Scanner tab implementation for the BugHunter application."""


class ScannerTab(BaseTab):
    """Scanner interface tab"""

    def __init__(self, _scanner: VulnerabilityScanner, _parent=None):
        self.scanner = scanner
        self.scan_in_progress = False
        self.logger = logging.get_logger("BugHunter.ScannerTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create target input section
            target_group = QGroupBox("Target")
            target_layout = QVBoxLayout()
            target_group.set_layout(target_layout)

            input_layout = QHBoxLayout()
            self.target_input = QLineEdit()
            self.target_input.set_placeholder_text("Enter target URL or IP")
            self.target_input.text_changed.connect(self._handle_input_change)

            self.scan_button = QPushButton("Start Scan")
            self.scan_button.clicked.connect(self._start_scan)
            self.scan_button.set_enabled(False)

            input_layout.add_widget(self.target_input)
            input_layout.add_widget(self.scan_button)
            target_layout.add_layout(input_layout)

            # Create scan options section
            options_group = QGroupBox("Scan Options")
            options_layout = QVBoxLayout()
            options_group.set_layout(options_layout)

            # Scan type selection
            scan_type_layout = QHBoxLayout()
            scan_type_label = QLabel("Scan Type:")
            self.scan_type_combo = QComboBox()
            self.scan_type_combo.add_items(
                ["Quick Scan", "Full Scan", "Custom Scan"])
            scan_type_layout.add_widget(scan_type_label)
            scan_type_layout.add_widget(self.scan_type_combo)
            options_layout.add_layout(scan_type_layout)

            # Progress section
            progress_group = QGroupBox("Progress")
            progress_layout = QVBoxLayout()
            progress_group.set_layout(progress_layout)

            self.progress_bar = QProgressBar()
            self.progress_bar.set_range(0, 100)
            self.progress_bar.set_value(0)

            self.status_label = QLabel("Ready")
            progress_layout.add_widget(self.progress_bar)
            progress_layout.add_widget(self.status_label)

            # Results section
            results_group = QGroupBox("Results")
            results_layout = QVBoxLayout()
            results_group.set_layout(results_layout)

            self.results_text = QTextEdit()
            self.results_text.set_read_only(True)
            self.results_text.set_placeholder_text(
                "Scan results will appear here...")
            results_layout.add_widget(self.results_text)

            # Add all components to main layout
            self.layout.add_widget(target_group)
            self.layout.add_widget(options_group)
            self.layout.add_widget(progress_group)
            self.layout.add_widget(results_group)

            # Add initial message
            self._update_status(
                "Scanner ready. Enter a target and click Start Scan.")

            def _handle_input_change(self):
                """Handle changes to target input"""
                # Enable scan button only if there's text and no scan in progress
                has_text = bool(self.target_input.text().strip())
                self.scan_button.set_enabled(
                    has_text and not self.scan_in_progress)

                def _update_status(self, _message: str):
                    """Update status message"""
                    self.status_label.set_text(message)
                    self.logger.info(message)

                    def _update_progress(self, _value: int):
                        """Update progress bar"""
                        self.progress_bar.set_value(value)

                        def _add_result(self, _text: str):
                            """Add text to results"""
                            self.results_text.append(text)

                            @pyqt_slot()
                            def _start_scan(self):
                                """Start the vulnerability scan"""
                                if self.scan_in_progress:
                                return

                                target = self.target_input.text().strip()
                                if not target:
                                    self._update_status(
                                        "Please enter a target URL or IP")
                                return

                                scan_type = self.scan_type_combo.current_text().lower().replace(" ", "_")

                                try:
                                    # Update UI state
                                    self.scan_in_progress = True
                                    self.scan_button.set_text("Scanning...")
                                    self.scan_button.set_enabled(False)
                                    self.target_input.set_enabled(False)
                                    self.scan_type_combo.set_enabled(False)
                                    self.progress_bar.set_value(0)
                                    self.results_text.clear()

                                    self._update_status(
                                        f"Starting {scan_type} on {target}...")

                                    # Start scan
                                    try:
                                        results = self.scanner.start_scan(
                                            target, scan_type)

                                        # Add results
                                        if isinstance(results, dict):
                                            for key, value in results.items():
                                                self._add_result(
                                                    f"{key}: {value}")
                                                else:
                                                    self._add_result(
                                                        str(results))

                                                    self._update_status(
                                                        "Scan completed successfully")
                                                    self._update_progress(100)

                                                    except Exception as e:
                                                        self._update_status(
                                                            f"Scan failed: {str(e)}")
                                                        self._add_result(
                                                            f"Error: {str(e)}")

                                                        finally:
                                                            # Reset UI state
                                                            self.scan_in_progress = False
                                                            self.scan_button.set_text(
                                                                "Start Scan")
                                                            self.scan_button.set_enabled(
                                                                True)
                                                            self.target_input.set_enabled(
                                                                True)
                                                            self.scan_type_combo.set_enabled(
                                                                True)

                                                            def refresh(self):
                                                                """Refresh tab content"""
                                                                if not self.scan_in_progress:
                                                                    self.target_input.clear()
                                                                    self.scan_type_combo.set_current_index(
                                                                        0)
                                                                    self.progress_bar.set_value(
                                                                        0)
                                                                    self.results_text.clear()
                                                                    self._update_status(
                                                                        "Scanner ready. Enter a target and click Start Scan.")
