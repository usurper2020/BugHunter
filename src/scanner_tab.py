from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLabel, QLineEdit, QComboBox, QProgressBar
)
from PyQt6.QtCore import Qt

class ScannerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the Scanner tab UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header
        header = QLabel("Vulnerability Scanner")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #ffffff;")
        layout.addWidget(header)

        # Target input section
        target_layout = QHBoxLayout()
        target_label = QLabel("Target:")
        target_label.setStyleSheet("color: #ffffff;")
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target URL or IP")
        self.target_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #2196f3;
            }
        """)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)

        # Scan type selection
        scan_type_layout = QHBoxLayout()
        scan_type_label = QLabel("Scan Type:")
        scan_type_label.setStyleSheet("color: #ffffff;")
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(["Quick Scan", "Full Scan", "Custom Scan"])
        self.scan_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid #666666;
                border-right: 5px solid #666666;
                border-top: 5px solid #ffffff;
                width: 0;
                height: 0;
            }
        """)
        scan_type_layout.addWidget(scan_type_label)
        scan_type_layout.addWidget(self.scan_type_combo)
        layout.addLayout(scan_type_layout)

        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Scan")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        
        # Button styles
        button_style = """
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #666666;
            }
        """
        self.start_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333333;
                border-radius: 4px;
                text-align: center;
                color: #ffffff;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #2196f3;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Results area
        results_label = QLabel("Scan Results:")
        results_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(results_label)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.results_display)

        # Connect signals
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)
        self.scan_type_combo.currentTextChanged.connect(self.on_scan_type_changed)

    def start_scan(self):
        """Start the vulnerability scan"""
        target = self.target_input.text().strip()
        if not target:
            self.results_display.append("Error: Please enter a target URL or IP")
            return

        scan_type = self.scan_type_combo.currentText()
        self.results_display.append(f"Starting {scan_type} on {target}...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)

    def stop_scan(self):
        """Stop the current scan"""
        self.results_display.append("Scan stopped by user")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_scan_type_changed(self, scan_type):
        """Handle scan type selection changes"""
        self.results_display.append(f"Scan type changed to: {scan_type}")

    def update_progress(self, value):
        """Update the progress bar"""
        self.progress_bar.setValue(value)

    def append_result(self, result):
        """Append a new result to the results display"""
        self.results_display.append(result)
