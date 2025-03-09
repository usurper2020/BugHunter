from .base_tab import BaseTab
from services.tool_manager import ToolManager
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


"""Amass tab implementation for the BugHunter application."""


class AmassTab(BaseTab):
    """Amass interface tab"""

    def __init__(self, _tool_manager: ToolManager, _parent=None):
        self.tool_manager = tool_manager
        self.logger = logging.get_logger("BugHunter.AmassTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create scan section
            scan_group = QGroupBox("Amass Scan")
            scan_layout = QVBoxLayout()
            scan_group.set_layout(scan_layout)

            input_layout = QHBoxLayout()
            self.domain_input = QLineEdit()
            self.domain_input.set_placeholder_text("Enter target domain...")

            self.scan_button = QPushButton("Start Scan")
            self.scan_button.clicked.connect(self._start_scan)

            input_layout.add_widget(self.domain_input)
            input_layout.add_widget(self.scan_button)

            self.scan_type_combo = QComboBox()
            self.scan_type_combo.add_items(
                ["Passive Scan", "Active Scan", "Full Enumeration"]
            )

            scan_layout.add_layout(input_layout)
            scan_layout.add_widget(self.scan_type_combo)

            # Create results section
            results_group = QGroupBox("Scan Results")
            results_layout = QVBoxLayout()
            results_group.set_layout(results_layout)

            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            self.results_display.set_placeholder_text(
                "Scan results will appear here...")
            results_layout.add_widget(self.results_display)

            # Add status section
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.set_layout(status_layout)

            self.status_label = QLabel("Ready")
            self.progress_bar = QProgressBar()
            self.progress_bar.set_range(0, 100)
            self.progress_bar.set_value(0)

            status_layout.add_widget(self.status_label)
            status_layout.add_widget(self.progress_bar)

            # Add all components to main layout
            self.layout.add_widget(scan_group)
            self.layout.add_widget(results_group)
            self.layout.add_widget(status_group)

            self._update_status("Amass scanner ready.")

            def _update_status(self, _message: str):
                """Update status message"""
                self.status_label.set_text(message)
                self.logger.info(message)

                def _update_progress(self, _value: int):
                    """Update progress bar"""
                    self.progress_bar.set_value(value)

                    def _display_results(self, _results):
                        """Display scan results"""
                        self.results_display.clear()
                        if isinstance(results, dict):
                            for key, value in results.items():
                                self.results_display.append(
                                    f"<b>{key}:</b> {value}")
                                else:
                                    self.results_display.append(str(results))

                                    @pyqt_slot()
                                    def _start_scan(self):
                                        """Handle Amass scan"""
                                        domain = self.domain_input.text().strip()
                                        if not domain:
                                            self._update_status(
                                                "Please enter a domain")
                                        return

                                        scan_type = self.scan_type_combo.current_text()
                                        try:
                                            self._update_status(
                                                f"Starting {scan_type}...")
                                            self._update_progress(0)

                                            # Start the scan
                                            amass = self.tool_manager.get_tool(
                                                "amass")
                                            results = amass.run_scan(
                                                domain, scan_type.lower())

                                            # Update UI with results
                                            self._display_results(results)
                                            self._update_progress(100)
                                            self._update_status(
                                                f"{scan_type} completed successfully")
                                            except Exception as e:
                                                self._update_status(
                                                    f"Error during scan: {str(e)}")
                                                self.logger.error(
                                                    f"Error during scan: {str(e)}")
                                                self._update_progress(0)

                                                def refresh(self):
                                                    """Refresh tab content"""
                                                    self.domain_input.clear()
                                                    self.results_display.clear()
                                                    self._update_progress(0)
                                                    self._update_status(
                                                        "Amass tab refreshed.")
