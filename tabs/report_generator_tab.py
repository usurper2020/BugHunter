"""
Report Generator tab for the BugHunter application.

This tab provides tools for generating comprehensive reports with real-time
status updates and progress tracking.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton, QSplitter, QProgressBar,
                           QComboBox, QFileDialog)
from PyQt6.QtCore import QTimer
from services.report_generator import ReportGenerator

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
        splitter.setOrientation(1)  # Vertical split
        
        # Top panel - Controls and input
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        # Report type selection
        self.report_type = QComboBox()
        self.report_type.addItems(["Vulnerability", "Scan", "Comprehensive"])
        top_layout.addWidget(QLabel("Report Type:"))
        top_layout.addWidget(self.report_type)
        
        # Template selection
        self.template_select = QComboBox()
        self.template_select.addItems(["Standard", "Detailed", "Executive"])
        top_layout.addWidget(QLabel("Template:"))
        top_layout.addWidget(self.template_select)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.toggle_generation)
        self.stop_button = QPushButton("Stop Generation")
        self.stop_button.clicked.connect(self.stop_generation)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.stop_button)
        top_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        top_layout.addWidget(self.progress_bar)
        
        # Bottom panel - Status and results
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # Status window
        self.status_window = QTextEdit()
        self.status_window.setReadOnly(True)
        self.status_window.setPlaceholderText("Status messages will appear here...")
        bottom_layout.addWidget(QLabel("Generation Status:"))
        bottom_layout.addWidget(self.status_window)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText("Report preview will appear here...")
        bottom_layout.addWidget(QLabel("Report Preview:"))
        bottom_layout.addWidget(self.results_display)
        
        # Add panels to splitter
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

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
            self.status_window.append("Initializing report generation...")
            
            # Configure UI for active generation
            self.generate_button.setText("Pause Generation")
            self.stop_button.setEnabled(True)
            self.progress_bar.setValue(0)
            
            # Start status updates
            self.status_timer.start(500)
            
            # Start the generation process
            report_type = self.report_type.currentText()
            template = self.template_select.currentText()
            
            self.generator.start_generation(
                report_type,
                template,
                progress_callback=self.update_progress,
                status_callback=self.update_status,
                result_callback=self.update_results
            )
            
        except Exception as e:
            self.status_window.append(f"Generation initialization failed: {str(e)}")
            self.generation_in_progress = False

    def pause_generation(self):
        """Pause the current report generation."""
        self.generator.pause_generation()
        self.generation_in_progress = False
        self.generate_button.setText("Resume Generation")
        self.status_window.append("Generation paused")

    def stop_generation(self):
        """Stop the current report generation."""
        self.generator.stop_generation()
        self.generation_in_progress = False
        self.generate_button.setText("Generate Report")
        self.stop_button.setEnabled(False)
        self.status_timer.stop()
        self.status_window.append("Generation stopped")
        self.progress_bar.setValue(0)

    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_bar.setValue(value)

    def update_status(self):
        """Update the status window with current generation information."""
        status = self.generator.get_status()
        self.status_window.append(status)

    def update_results(self, result):
        """Update the results display with new report content."""
        self.results_display.append(result)

    def save_report(self):
        """Save the generated report to a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "",
            "PDF Files (*.pdf);;HTML Files (*.html);;Text Files (*.txt)",
            options=options
        )
        
        if file_name:
            try:
                self.generator.save_report(file_name)
                self.status_window.append(f"Report successfully saved to {file_name}")
            except Exception as e:
                self.status_window.append(f"Failed to save report: {str(e)}")
