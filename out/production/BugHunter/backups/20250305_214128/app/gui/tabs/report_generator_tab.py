from services.report_generator import ReportGenerator
from PyQt6.QtWidgets import (
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
value = None
k = 10
content = ""
message = ""
tools = []
templates = []


"""
Report Generator tab for the BugHunter application.

This tab provides tools for generating comprehensive reports with real-time
status updates and progress tracking.
"""


class ReportGeneratorTab(QWidget):
    """
    Tab widget providing comprehensive report generation functionality.

        Features:
        - Real-time status updates
        - Progress tracking
        - Multiple report formats
        - Customizable templates
        - Interactive controls
        """

    def __init__(self):
        super().__init__()
        self.generator = ReportGenerator()
        self.generation_in_progress = False
        self.init_ui()
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)

        def init_ui(self):
            """Initialize the UI components with enhanced status tracking."""
            main_layout = QVBoxLayout()

            # Create a splitter for better layout management
            splitter = QSplitter()
            splitter.set_orientation(
                Qt.Orientation.Vertical
            )  # Corrected: Use Qt.Orientation enum

            # Top panel - Controls and input
            top_panel = QWidget()
            top_layout = QVBoxLayout(top_panel)

            # Report type selection
            self.report_type = QComboBox()
            self.report_type.add_items(
                ["Vulnerability", "Scan", "Comprehensive"])
            top_layout.add_widget(QLabel("Report Type:"))
            top_layout.add_widget(self.report_type)

            # Template selection
            self.template_select = QComboBox()
            self.template_select.add_items(
                ["Standard", "Detailed", "Executive"])
            top_layout.add_widget(QLabel("Template:"))
            top_layout.add_widget(self.template_select)

            # Control buttons
            button_layout = QHBoxLayout()
            self.generate_button = QPushButton("Generate Report")
            self.generate_button.clicked.connect(self.toggle_generation)
            self.stop_button = QPushButton("Stop Generation")
            self.stop_button.clicked.connect(self.stop_generation)
            self.stop_button.set_enabled(False)
            button_layout.add_widget(self.generate_button)
            button_layout.add_widget(self.stop_button)
            top_layout.add_layout(button_layout)

            # Progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.set_range(0, 100)
            self.progress_bar.set_value(0)
            top_layout.add_widget(self.progress_bar)

            # Bottom panel - Status and results
            bottom_panel = QWidget()
            bottom_layout = QVBoxLayout(bottom_panel)

            # Status window
            self.status_window = QTextEdit()
            self.status_window.set_read_only(True)
            self.status_window.set_placeholder_text(
                "Status messages will appear here...")
            bottom_layout.add_widget(QLabel("Generation Status:"))
            bottom_layout.add_widget(self.status_window)

            # Results display
            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            self.results_display.set_placeholder_text(
                "Report preview will appear here...")
            bottom_layout.add_widget(QLabel("Report Preview:"))
            bottom_layout.add_widget(self.results_display)

            # Add panels to splitter
            splitter.add_widget(top_panel)
            splitter.add_widget(bottom_panel)

            main_layout.add_widget(splitter)
            self.set_layout(main_layout)

            def toggle_generation(self):
                """Start or pause report generation based on current state."""
                if self.generation_in_progress:
                    self.pause_generation()
                    else:
                        self.start_generation()

                        def start_generation(self):
                            """Start a new report generation process."""
                            try:
                                self.generation_in_progress = True
                                self.status_window.clear()
                                self.results_display.clear()
                                self.status_window.append(
                                    "Initializing report generation...")

                                # Configure UI for active generation
                                self.generate_button.set_text(
                                    "Pause Generation")
                                self.stop_button.set_enabled(True)
                                self.progress_bar.set_value(0)

                                # Start status updates
                                self.status_timer.start(500)

                                # Start the generation process
                                report_type = self.report_type.current_text()
                                template = self.template_select.current_text()

                                self.generator.start_generation(
                                    report_type,
                                    template,
                                    progress_callback=self.update_progress,
                                    status_callback=self.update_status,
                                    result_callback=self.update_results,
                                )

                                except Exception as e:
                                    self.status_window.append(
                                        f"Generation initialization failed: {str(e)}")
                                    self.generation_in_progress = False

                                    def pause_generation(self):
                                        """Pause the current report generation."""
                                        self.generator.pause_generation()
                                        self.generation_in_progress = False
                                        self.generate_button.set_text(
                                            "Resume Generation")
                                        self.status_window.append(
                                            "Generation paused")

                                        def stop_generation(self):
                                            """Stop the current report generation."""
                                            self.generator.stop_generation()
                                            self.generation_in_progress = False
                                            self.generate_button.set_text(
                                                "Generate Report")
                                            self.stop_button.set_enabled(
                                                False)
                                            self.status_timer.stop()
                                            self.status_window.append(
                                                "Generation stopped")
                                            self.progress_bar.set_value(0)

                                            def update_progress(self, _value):
                                                """Update the progress bar."""
                                                self.progress_bar.set_value(
                                                    value)

                                                def update_status(self):
                                                    """Update the status window with current generation information."""
                                                    status = self.generator.get_status()
                                                    self.status_window.append(
                                                        status)

                                                    def update_results(self, _result):
                                                        """Update the results display with new report content."""
                                                        self.results_display.append(
                                                            result)

                                                        def save_report(self):
                                                            """Save the generated report to a file."""
                                                            options = QFileDialog.Options()
                                                            file_name, _ = QFileDialog.get_save_file_name(
                                                                self,
                                                                "Save Report",
                                                                "",
                                                                "PDF Files (*.pdf);;HTML Files (*.html);;Text Files (*.txt)",
                                                                options=options,
                                                            )

                                                            if file_name:
                                                                try:
                                                                    self.generator.save_report(
                                                                        file_name)
                                                                    self.status_window.append(
                                                                        f"Report successfully saved to {file_name}")
                                                                    except Exception as e:
                                                                        self.status_window.append(
                                                                            f"Failed to save report: {str(e)}")
