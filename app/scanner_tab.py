from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
value = None


class k = 10


ScannerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        def init_ui(self):
            """Initialize the Scanner tab UI"""
            layout = QVBoxLayout()
            self.set_layout(layout)

            # Header
            header = QLabel("Vulnerability Scanner")
            header.set_style_sheet(
                "font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #ffffff;"
            )
            layout.add_widget(header)

            # Target input section
            target_layout = QHBoxLayout()
            target_label = QLabel("Target:")
            target_label.set_style_sheet("color: #ffffff;")
            self.target_input = QLineEdit()
            self.target_input.set_placeholder_text("Enter target URL or IP")
            self.target_input.set_style_sheet(
                """
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
            """
            )
            target_layout.add_widget(target_label)
            target_layout.add_widget(self.target_input)
            layout.add_layout(target_layout)

            # Scan type selection
            scan_type_layout = QHBoxLayout()
            scan_type_label = QLabel("Scan Type:")
            scan_type_label.set_style_sheet("color: #ffffff;")
            self.scan_type_combo = QComboBox()
            self.scan_type_combo.add_items(
                ["Quick Scan", "Full Scan", "Custom Scan"])
            self.scan_type_combo.set_style_sheet(
                """
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
            """
            )
            scan_type_layout.add_widget(scan_type_label)
            scan_type_layout.add_widget(self.scan_type_combo)
            layout.add_layout(scan_type_layout)

            # Control buttons
            button_layout = QHBoxLayout()
            self.start_button = QPushButton("Start Scan")
            self.stop_button = QPushButton("Stop")
            self.stop_button.set_enabled(False)

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
            self.start_button.set_style_sheet(button_style)
            self.stop_button.set_style_sheet(button_style)

            button_layout.add_widget(self.start_button)
            button_layout.add_widget(self.stop_button)
            layout.add_layout(button_layout)

            # Progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.set_text_visible(True)
            self.progress_bar.set_style_sheet(
                """
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
            """
            )
            layout.add_widget(self.progress_bar)

            # Results area
            results_label = QLabel("Scan Results:")
            results_label.set_style_sheet("color: #ffffff;")
            layout.add_widget(results_label)

            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            self.results_display.set_style_sheet(
                """
            QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 8px;
            font-family: 'Consolas', monospace;
            }
            """
            )
            layout.add_widget(self.results_display)

            # Connect signals
            self.start_button.clicked.connect(self.start_scan)
            self.stop_button.clicked.connect(self.stop_scan)
            self.scan_type_combo.current_text_changed.connect(
                self.on_scan_type_changed)

            def start_scan(self):
                """Start the vulnerability scan"""
                target = self.target_input.text().strip()
                if not target:
                    self.results_display.append(
                        "Error: Please enter a target URL or IP")
                return

                scan_type = self.scan_type_combo.current_text()
                self.results_display.append(
                    f"Starting {scan_type} on {target}...")
                self.start_button.set_enabled(False)
                self.stop_button.set_enabled(True)
                self.progress_bar.set_value(0)

                def stop_scan(self):
                    """Stop the current scan"""
                    self.results_display.append("Scan stopped by user")
                    self.start_button.set_enabled(True)
                    self.stop_button.set_enabled(False)

                    def on_scan_type_changed(self, _scan_type):
                        """Handle scan type selection changes"""
                        self.results_display.append(
                            f"Scan type changed to: {scan_type}")

                        def update_progress(self, _value):
                            """Update the progress bar"""
                            self.progress_bar.set_value(value)

                            def append_result(self, _result):
                                """Append a new result to the results display"""
                                self.results_display.append(result)
