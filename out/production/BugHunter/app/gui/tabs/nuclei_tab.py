from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

"""Nuclei tab implementation for the BugHunter application."""

import logging

from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from services.vulnerability_scanner import VulnerabilityScanner

from .base_tab import BaseTab


class NucleiTab(BaseTab):
    """Nuclei interface tab"""

    def __init__(self, _vulnerability_scanner: VulnerabilityScanner, _parent=None):
        self.scanner = vulnerability_scanner
        self.logger = logging.getLogger("BugHunter.NucleiTab")
        super().__init__(parent)

        def _setup_ui(self):
        """Setup the UI components"""
        # Create scan section
        scan_group = QGroupBox("Nuclei Scan")
        scan_layout = QVBoxLayout()
        scan_group.setLayout(scan_layout)

        input_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target URL or IP...")

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self._start_scan)

        input_layout.addWidget(self.target_input)
        input_layout.addWidget(self.scan_button)

        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(
            ["Full Scan", "Quick Scan", "Custom Scan"])

        scan_layout.addLayout(input_layout)
        scan_layout.addWidget(self.scan_type_combo)

        # Create results section
        results_group = QGroupBox("Scan Results")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText(
            "Scan results will appear here...")
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

        self._update_status("Nuclei scanner ready.")

        def _update_status(self, _message: str):
        """Update status message"""
        self.status_label.setText(message)
        self.logger.info(message)

        def _update_progress(self, _value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)

        def _display_results(self, _results):
        """Display scan results"""
        self.results_display.clear()
        if isinstance(results, dict):
                for key, value in results.items():
                self.results_display.append(f"<b>{key}:</b> {value}")
            else:
            self.results_display.append(str(results))

            @pyqtSlot()
        def _start_scan(self):
        """Handle Nuclei scan"""
        target = self.target_input.text().strip()
        if not target:
            self._update_status("Please enter a target")
        return

        scan_type = self.scan_type_combo.currentText()
        try:
            self._update_status(f"Starting {scan_type}...")
            self._update_progress(0)

            # Start the scan
            results = self.scanner.nuclei_scan(target, scan_type.lower())

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
        self.target_input.clear()
        self.results_display.clear()
        self._update_progress(0)
        self._update_status("Nuclei tab refreshed.")