# tabs/scanner_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QTextEdit,
    QProgressBar, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
import asyncio
from typing import Optional
from services.vulnerability_scanner import VulnerabilityScanner, ScanTarget
import json

class ScannerTab(QWidget):
    def __init__(self, scanner: Optional[VulnerabilityScanner] = None):
        super().__init__()
        self.scanner = scanner or VulnerabilityScanner()
        self.current_scan_id: Optional[str] = None
        self.status_timer: Optional[QTimer] = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the scanner tab UI"""
        layout = QVBoxLayout()

        # Target input section
        target_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target URL or IP")
        target_layout.addWidget(QLabel("Target:"))
        target_layout.addWidget(self.target_input)

        # Scan type selection
        self.scan_type = QComboBox()
        self.scan_type.addItems(['full', 'recon', 'vuln', 'port'])
        target_layout.addWidget(QLabel("Scan Type:"))
        target_layout.addWidget(self.scan_type)

        # Start scan button
        self.start_button = QPushButton("Start Scan")
        self.start_button.clicked.connect(self.start_scan)
        target_layout.addWidget(self.start_button)

        layout.addLayout(target_layout)

        # Progress section
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        layout.addLayout(progress_layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Vulnerability", "Severity", "Description", "Proof", "Tool"
        ])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.results_table)

        # Details section
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(QLabel("Details:"))
        layout.addWidget(self.details_text)

        self.setLayout(layout)

    async def start_scan(self):
        """Start a new vulnerability scan"""
        target_url = self.target_input.text().strip()
        if not target_url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL")
            return

        try:
            # Create scan target
            target = ScanTarget(url=target_url)
            
            # Start scan
            self.current_scan_id = await self.scanner.start_scan(
                target, 
                self.scan_type.currentText()
            )
            
            # Update UI
            self.start_button.setEnabled(False)
            self.status_label.setText("Scanning...")
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Start status update timer
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.update_scan_status)
            self.status_timer.start(1000)  # Update every second

        except Exception as e:
            QMessageBox.critical(self, "Scan Error", str(e))

    async def update_scan_status(self):
        """Update the scan status and results"""
        if not self.current_scan_id:
            return

        try:
            status = await self.scanner.get_scan_status(self.current_scan_id)
            
            if status['status'] == 'completed':
                self.status_timer.stop()
                self.progress_bar.setRange(0, 100)
                self.progress_bar.setValue(100)
                self.status_label.setText("Scan completed")
                self.start_button.setEnabled(True)
                await self.load_scan_results()
                
            elif status['status'] == 'failed':
                self.status_timer.stop()
                self.status_label.setText("Scan failed")
                self.start_button.setEnabled(True)
                QMessageBox.critical(self, "Scan Error", status.get('error', 'Unknown error'))
                
            elif status['status'] == 'cancelled':
                self.status_timer.stop()
                self.status_label.setText("Scan cancelled")
                self.start_button.setEnabled(True)

        except Exception as e:
            self.logger.error(f"Failed to update scan status: {e}")

    async def load_scan_results(self):
        """Load and display scan results"""
        try:
            results = await self.scanner.get_scan_results(self.current_scan_id)
            
            # Clear existing results
            self.results_table.setRowCount(0)
            
            # Add new results
            for finding in results['findings']:
                row = self.results_table.rowCount()
                self.results_table.insertRow(row)
                
                self.results_table.setItem(row, 0, QTableWidgetItem(finding['vulnerability_type']))
                self.results_table.setItem(row, 1, QTableWidgetItem(finding['severity']))
                self.results_table.setItem(row, 2, QTableWidgetItem(finding['description']))
                self.results_table.setItem(row, 3, QTableWidgetItem(finding['proof']))
                self.results_table.setItem(row, 4, QTableWidgetItem(finding['tool']))

            # Update details text
            self.details_text.setText(json.dumps(results, indent=2))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load scan results: {e}")

    def closeEvent(self, event):
        """Handle tab close event"""
        if self.current_scan_id and self.status_timer and self.status_timer.isActive():
            reply = QMessageBox.question(
                self,
                'Confirm Exit',
                'A scan is currently running. Do you want to stop it?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                asyncio.create_task(self.scanner.stop_scan(self.current_scan_id))
                self.status_timer.stop()
            else:
                event.ignore()
                return

        event.accept()
