from PyQt6.QtGui import QColor
from fpdf import FPDF
from collections import defaultdict
import json
import csv
from PyQt6.QtWidgets import (
QLabel,
QLineEdit,
QMessageBox,
QProgressBar,
QPushButton,
QTextEdit,
QVBoxLayout,
QWidget,
)
from typing import Dict, List
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
default = None
value = None
key = ""
vulnerabilities = []
k = 10
content = ""
message = ""
resources = []
items = []
recommendations = []


"""
Report Generator Module.

This module provides the report generation interface for BugHunter,
handling scan results and generating various report formats.

    Classes:
    ReportGeneratorTab: Report generator tab class.
    PDFReport: Custom PDF report class.
    """

    class ReportGeneratorTab(QWidget):
        def __init__(self):
        super().__init__()
        self.generator = ReportGenerator()
        self.generation_in_progress = False
        self.init_ui()
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)

            def init_ui(self):
            main_layout = QVBoxLayout()
            splitter = QSplitter()
            splitter.set_orientation(1)
            top_panel = QWidget()
            top_layout = QVBoxLayout(top_panel)
            self.report_type = QComboBox()
            self.report_type.add_items(
            ["Vulnerability", "Scan", "Comprehensive"])
            top_layout.add_widget(QLabel("Report Type:"))
            top_layout.add_widget(self.report_type)
            self.template_select = QComboBox()
            self.template_select.add_items(
            ["Standard", "Detailed", "Executive"])
            top_layout.add_widget(QLabel("Template:"))
            top_layout.add_widget(self.template_select)
            button_layout = QHBoxLayout()
            self.generate_button = QPushButton("Generate Report")
            self.generate_button.clicked.connect(self.toggle_generation)
            self.stop_button = QPushButton("Stop Generation")
            self.stop_button.clicked.connect(self.stop_generation)
            self.stop_button.set_enabled(False)
            button_layout.add_widget(self.generate_button)
            button_layout.add_widget(self.stop_button)
            top_layout.add_layout(button_layout)
            self.progress_bar = QProgressBar()
            self.progress_bar.set_range(0, 100)
            self.progress_bar.set_value(0)
            top_layout.add_widget(self.progress_bar)
            bottom_panel = QWidget()
            bottom_layout = QVBoxLayout(bottom_panel)
            self.status_window = QTextEdit()
            self.status_window.set_read_only(True)
            self.status_window.set_placeholder_text(
            "Status messages will appear here...")
            bottom_layout.add_widget(QLabel("Generation Status:"))
            bottom_layout.add_widget(self.status_window)
            self.results_display = QTextEdit()
            self.results_display.set_read_only(True)
            self.results_display.set_placeholder_text(
            "Report preview will appear here...")
            bottom_layout.add_widget(QLabel("Report Preview:"))
            bottom_layout.add_widget(self.results_display)
            splitter.add_widget(top_panel)
            splitter.add_widget(bottom_panel)
            main_layout.add_widget(splitter)
            self.set_layout(main_layout)

                def toggle_generation(self):
                    if self.generation_in_progress:
                    self.pause_generation()
                        else:
                        self.start_generation()

                            def start_generation(self):
                                try:
                                self.generation_in_progress = True
                                self.status_window.clear()
                                self.results_display.clear()
                                self.status_window.append(
                                "Initializing report generation...")
                                self.generate_button.set_text(
                                "Pause Generation")
                                self.stop_button.set_enabled(True)
                                self.progress_bar.set_value(0)
                                self.status_timer.start(500)
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
                                        self.generator.pause_generation()
                                        self.generation_in_progress = False
                                        self.generate_button.set_text(
                                        "Resume Generation")
                                        self.status_window.append(
                                        "Generation paused")

                                            def stop_generation(self):
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
                                                self.progress_bar.set_value(
                                                value)

                                                    def update_status(self):
                                                    status = self.generator.get_status()
                                                    self.status_window.append(
                                                    status)

                                                        def update_results(self, _result):
                                                        self.results_display.append(
                                                        result)

                                                            def save_report(self):
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

                                                                            class ReportGeneratorTab(QWidget):
                                                                            """
                                                                            Report generator tab for BugHunter.

                                                                                    Attributes:
                                                                                    results_table (QTableWidget): Table for displaying scan results.
                                                                                    export_combo (QComboBox): Dropdown for selecting export format.
                                                                                    export_button (QPushButton): Button to export report.
                                                                                    template_combo (QComboBox): Dropdown for selecting report template.
                                                                                    title_input (QLineEdit): Input for report title.
                                                                                    author_input (QLineEdit): Input for report author.
                                                                                    style_button (QPushButton): Button to customize report style.
                                                                                    """

                                                                                    report_generated = pyqt_signal(
                                                                                    str)

                                                                                def __init__(self):
                                                                                """Initialize the report generator tab."""
                                                                                super().__init__()
                                                                                self.scan_results = []
                                                                                self.init_ui()
                                                                                self.connect_signals()

                                                                                    def init_ui(self):
                                                                                    """Initialize the user interface components."""
                                                                                    layout = QVBoxLayout()

                                                                                    # Report metadata
                                                                                    meta_layout = QHBoxLayout()
                                                                                    meta_layout.add_widget(
                                                                                    QLabel("Title:"))
                                                                                    self.title_input = QLineEdit()
                                                                                    self.title_input.set_placeholder_text(
                                                                                    "Enter report title")
                                                                                    meta_layout.add_widget(
                                                                                    self.title_input)

                                                                                    meta_layout.add_widget(
                                                                                    QLabel("Author:"))
                                                                                    self.author_input = QLineEdit()
                                                                                    self.author_input.set_placeholder_text(
                                                                                    "Enter author name")
                                                                                    meta_layout.add_widget(
                                                                                    self.author_input)
                                                                                    layout.add_layout(
                                                                                    meta_layout)

                                                                                    # Results table
                                                                                    self.results_table = QTableWidget()
                                                                                    self.results_table.set_column_count(
                                                                                    4)
                                                                                    self.results_table.set_horizontal_header_labels(
                                                                                    ["Target", "Vulnerability", "Severity", "Details"]
                                                                                    )
                                                                                    header = self.results_table.horizontal_header()
                                                                                    header.set_section_resize_mode(
                                                                                    0, QHeaderView.ResizeMode.ResizeToContents)
                                                                                    header.set_section_resize_mode(
                                                                                    1, QHeaderView.ResizeMode.Stretch)
                                                                                    header.set_section_resize_mode(
                                                                                    2, QHeaderView.ResizeMode.ResizeToContents)
                                                                                    header.set_section_resize_mode(
                                                                                    3, QHeaderView.ResizeMode.Stretch)
                                                                                    layout.add_widget(
                                                                                    self.results_table)

                                                                                    # Export controls
                                                                                    export_layout = QHBoxLayout()
                                                                                    export_layout.add_widget(
                                                                                    QLabel("Export Format:"))

                                                                                    self.export_combo = QComboBox()
                                                                                    self.export_combo.add_items(
                                                                                    ["JSON", "CSV", "PDF"])
                                                                                    export_layout.add_widget(
                                                                                    self.export_combo)

                                                                                    export_layout.add_widget(
                                                                                    QLabel("Template:"))
                                                                                    self.template_combo = QComboBox()
                                                                                    self.template_combo.add_items(
                                                                                    ["Basic", "Detailed", "Executive", "Technical"])
                                                                                    export_layout.add_widget(
                                                                                    self.template_combo)

                                                                                    self.style_button = QPushButton(
                                                                                    "Customize Style")
                                                                                    export_layout.add_widget(
                                                                                    self.style_button)

                                                                                    self.export_button = QPushButton(
                                                                                    "Export Report")
                                                                                    export_layout.add_widget(
                                                                                    self.export_button)

                                                                                    layout.add_layout(
                                                                                    export_layout)
                                                                                    self.set_layout(
                                                                                    layout)

                                                                                        def connect_signals(self):
                                                                                        """Connect UI signals to appropriate slots."""
                                                                                        self.export_button.clicked.connect(
                                                                                        self.export_report)
                                                                                        self.style_button.clicked.connect(
                                                                                        self.customize_style)

                                                                                            def add_scan_result(self, _result):
                                                                                            """Add a scan result to the report.

                                                                                                        Args:
                                                                                                        result (dict): Scan result to add.
                                                                                                        """
                                                                                                        self.scan_results.append(
                                                                                                        result)
                                                                                                        self.update_results_table()

                                                                                                def update_results_table(self):
                                                                                                """Update the results table with current scan results."""
                                                                                                self.results_table.set_row_count(
                                                                                                len(self.scan_results))

                                                                                                    for row, result in enumerate(self.scan_results):
                                                                                                    self.results_table.set_item(
                                                                                                    row, 0, QTableWidgetItem(
                                                                                                    result.get("target", ""))
                                                                                                    )
                                                                                                    self.results_table.set_item(
                                                                                                    row, 1, QTableWidgetItem(
                                                                                                    result.get("vulnerability", ""))
                                                                                                    )
                                                                                                    self.results_table.set_item(
                                                                                                    row, 2, QTableWidgetItem(
                                                                                                    result.get("severity", ""))
                                                                                                    )
                                                                                                    self.results_table.set_item(
                                                                                                    row, 3, QTableWidgetItem(
                                                                                                    result.get("details", ""))
                                                                                                    )

                                                                                                        def export_report(self):
                                                                                                        """Export the report in the selected format."""
                                                                                                        export_format = self.export_combo.current_text()
                                                                                                        file_path, _ = QFileDialog.get_save_file_name(
                                                                                                        self,
                                                                                                        "Save Report",
                                                                                                        "",
                                                                                                        f"{export_format} Files (*.{export_format.lower()})",
                                                                                                        )

                                                                                                            if file_path:
                                                                                                                try:
                                                                                                                    if export_format == "JSON":
                                                                                                                    self.export_json(
                                                                                                                    file_path)
                                                                                                                        elif export_format == "CSV":
                                                                                                                        self.export_csv(
                                                                                                                        file_path)
                                                                                                                            elif export_format == "PDF":
                                                                                                                            self.export_pdf(
                                                                                                                            file_path)

                                                                                                                            self.report_generated.emit(
                                                                                                                            f"Report successfully exported to {file_path}"
                                                                                                                            )
                                                                                                                                except Exception as e:
                                                                                                                                QMessageBox.critical(
                                                                                                                                self, "Export Error", f"Failed to export report: {str(e)}"
                                                                                                                                )

                                                                                                                                    def customize_style(self):
                                                                                                                                    """Open style customization dialog."""
                                                                                                                                    color = QColorDialog.get_color()
                                                                                                                                        if color.is_valid():
                                                                                                                                        self.apply_style(
                                                                                                                                        color)

                                                                                                                                            def apply_style(self, _color):
                                                                                                                                            """Apply custom style to the report.

                                                                                                                                                            Args:
                                                                                                                                                            color (QColor): Selected color for styling.
                                                                                                                                                            """
                                                                                                                                                            stylesheet = f"""
                                                                                                                                                            QWidget {{
                                                                                                                                                            background-color: {color.name()};
                                                                                                                                                            color: #000000;
                                                                                                                                                            font-family: Arial, sans-serif;
                                                                                                                                                            font-size: 12pt;
                                                                                                                                                            }}
                                                                                                                                                            QTableWidget {{
                                                                                                                                                            background-color: #FFFFFF;
                                                                                                                                                            alternate-background-color: #F0F0F0;
                                                                                                                                                            }}
                                                                                                                                                            QHeaderView::section {{
                                                                                                                                                            background-color: {color.name()};
                                                                                                                                                            color: #FFFFFF;
                                                                                                                                                            font-weight: bold;
                                                                                                                                                            }}
                                                                                                                                                            QPushButton {{
                                                                                                                                                            background-color: {color.name()};
                                                                                                                                                            color: #FFFFFF;
                                                                                                                                                            border: 1px solid #000000;
                                                                                                                                                            padding: 5px;
                                                                                                                                                            }}
                                                                                                                                                            """
                                                                                                                                                            self.set_style_sheet(
                                                                                                                                                            stylesheet)

                                                                                                                                                def export_json(self, _file_path):
                                                                                                                                                """Export report as JSON.

                                                                                                                                                                    Args:
                                                                                                                                                                    file_path (str): Path to save the JSON file.
                                                                                                                                                                    """
                                                                                                                                                                    report_data = self.get_report_metadata()
                                                                                                                                                                    report_data[
                                                                                                                                                                    "findings"] = self.scan_results

                                                                                                                                                    with open(file_path, "w", encoding="utf-8") as f:
                                                                                                                                                    json.dump(
                                                                                                                                                    report_data, f, indent=4)

                                                                                                                                                        def export_csv(self, _file_path):
                                                                                                                                                        """Export report as CSV.

                                                                                                                                                                                Args:
                                                                                                                                                                                file_path (str): Path to save the CSV file.
                                                                                                                                                                                """
                                                                                                                                                            with open(file_path, "w", newline="", encoding="utf-8") as f:
                                                                                                                                                            writer = csv.DictWriter(
                                                                                                                                                            f, fieldnames=[
                                                                                                                                                            "target", "vulnerability", "severity", "details"]
                                                                                                                                                            )
                                                                                                                                                            writer.writeheader()
                                                                                                                                                            writer.writerows(
                                                                                                                                                            self.scan_results)

                                                                                                                                                                def export_pdf(self, _file_path):
                                                                                                                                                                """Export report as PDF.

                                                                                                                                                                                            Args:
                                                                                                                                                                                            file_path (str): Path to save the PDF file.
                                                                                                                                                                                            """
                                                                                                                                                                                            template = self.template_combo.current_text()
                                                                                                                                                                                            pdf = PDFReport(
                                                                                                                                                                                            template)
                                                                                                                                                                                            pdf.set_metadata(
                                                                                                                                                                                            **self.get_report_metadata())

                                                                                                                                                                    if template == "Executive":
                                                                                                                                                                    pdf.add_executive_summary(
                                                                                                                                                                    self.scan_results)
                                                                                                                                                                    pdf.add_recommendations(
                                                                                                                                                                    self.scan_results)
                                                                                                                                                                        elif template == "Technical":
                                                                                                                                                                        pdf.add_technical_details(
                                                                                                                                                                        self.scan_results)
                                                                                                                                                                        pdf.add_appendix(
                                                                                                                                                                        self.scan_results)
                                                                                                                                                                            else:
                                                                                                                                                                            pdf.add_findings(
                                                                                                                                                                            self.scan_results)

                                                                                                                                                                            pdf.output(
                                                                                                                                                                            file_path)

                                                                                                                                                                                def get_report_metadata(self):
                                                                                                                                                                                """Get report metadata.

                                                                                                                                                                                                                Returns:
                                                                                                                                                                                                                dict: Dictionary containing report metadata.
                                                                                                                                                                                                                """
                                                                                                                                                                                return {
                                                                                                                                                                                "title": self.title_input.text() or "BugHunter Report",
                                                                                                                                                                                "author": self.author_input.text() or "BugHunter",
                                                                                                                                                                                "date": QDate.current_date().to_string("yyyy-MM-dd"),
                                                                                                                                                                                }

                                                                                                                                                                                    def cleanup(self):
                                                                                                                                                                                    """Clean up resources before closing."""
                                                                                                                                                                                    self.scan_results.clear()
                                                                                                                                                                                    self.results_table.set_row_count(
                                                                                                                                                                                    0)

                                                                                                                                                                                        class PDFReport(FPDF):
                                                                                                                                                                                        """Custom PDF report class."""

                                                                                                                                                                                            def __init__(self, _template="Basic"):
                                                                                                                                                                                            """Initialize the PDF report.

                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                            template (str): Template to use for the report.
                                                                                                                                                                                                                            """
                                                                                                                                                                                                                            super().__init__()
                                                                                                                                                                                                                            self.template = template
                                                                                                                                                                                                                            self.set_auto_page_break(
                                                                                                                                                                                                                            auto=True, margin=15)
                                                                                                                                                                                                                            self.add_page()
                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                            "Arial", "", 12)
                                                                                                                                                                                                                            self.colors = {
                                                                                                                                                                                                                            "header": (0, 51, 102),
                                                                                                                                                                                                                            "critical": (255, 0, 0),
                                                                                                                                                                                                                            "high": (255, 128, 0),
                                                                                                                                                                                                                            "medium": (255, 255, 0),
                                                                                                                                                                                                                            "low": (0, 128, 0),
                                                                                                                                                                                                                            }

                                                                                                                                                                                                def header(self):
                                                                                                                                                                                                """Add header to each page."""
                                                                                                                                                                                                self.set_font(
                                                                                                                                                                                                "Arial", "B", 16)
                                                                                                                                                                                                self.set_text_color(
                                                                                                                                                                                                *self.colors["header"])
                                                                                                                                                                                                self.cell(
                                                                                                                                                                                                0, 10, self.title, 0, 1, "C")
                                                                                                                                                                                                self.set_font(
                                                                                                                                                                                                "Arial", "", 12)
                                                                                                                                                                                                self.set_text_color(
                                                                                                                                                                                                0, 0, 0)
                                                                                                                                                                                                self.cell(
                                                                                                                                                                                                0, 10, f"Author: {self.author} | Date: {self.date}", 0, 1, "C")
                                                                                                                                                                                                self.ln(
                                                                                                                                                                                                10)

                                                                                                                                                                                                    def footer(self):
                                                                                                                                                                                                    """Add footer to each page."""
                                                                                                                                                                                                    self.set_y(
                                                                                                                                                                                                    -15)
                                                                                                                                                                                                    self.set_font(
                                                                                                                                                                                                    "Arial", "I", 8)
                                                                                                                                                                                                    self.cell(
                                                                                                                                                                                                    0, 10, f"Page {self.page_no()}", 0, 0, "C")

                                                                                                                                                                                                        def add_executive_summary(self, _findings):
                                                                                                                                                                                                        """Add executive summary section.

                                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                                            findings (list): List of scan findings.
                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                            "Arial", "B", 14)
                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                            0, 10, "Executive Summary", 0, 1)
                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                            # Calculate statistics
                                                                                                                                                                                                                                            severity_counts = defaultdict(
                                                                                                                                                                                                                                            int)
                                                                                                                                                                                                            for finding in findings:
                                                                                                                                                                                                            severity_counts[finding.get(
                                                                                                                                                                                                            "severity", "Unknown")] += 1

                                                                                                                                                                                                            # Add summary content
                                                                                                                                                                                                            self.multi_cell(
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            10,
                                                                                                                                                                                                            f"This report summarizes the findings from the security scan conducted on {self.date}. "
                                                                                                                                                                                                            "The following key metrics were identified:",
                                                                                                                                                                                                            )
                                                                                                                                                                                                            self.ln(
                                                                                                                                                                                                            5)

                                                                                                                                                                                                                for severity, count in severity_counts.items():
                                                                                                                                                                                                                self.cell(
                                                                                                                                                                                                                0, 10, f"- {severity} severity findings: {count}", 0, 1)

                                                                                                                                                                                                                self.ln(
                                                                                                                                                                                                                10)

                                                                                                                                                                                                                    def add_recommendations(self, _findings):
                                                                                                                                                                                                                    """Add recommendations section.

                                                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                                                            findings (list): List of scan findings.
                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                            "Arial", "B", 14)
                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                            0, 10, "Recommendations", 0, 1)
                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                                            # Add general recommendations
                                                                                                                                                                                                                                                            self.multi_cell(
                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                            10,
                                                                                                                                                                                                                                                            "Based on the findings, the following recommendations are proposed:\n"
                                                                                                                                                                                                                                                            "1. Address critical and high severity findings immediately\n"
                                                                                                                                                                                                                                                            "2. Review medium severity findings for potential risks\n"
                                                                                                                                                                                                                                                            "3. Monitor low severity findings for future improvements\n"
                                                                                                                                                                                                                                                            "4. Implement regular security audits\n"
                                                                                                                                                                                                                                                            "5. Establish a vulnerability management process",
                                                                                                                                                                                                                                                            )
                                                                                                                                                                                                                                                            self.ln(
                                                                                                                                                                                                                                                            10)

                                                                                                                                                                                                                                                            # Add specific recommendations by severity
                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                            "Arial", "B", 12)
                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                            0, 10, "Detailed Recommendations by Severity:", 0, 1)
                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                                            severity_recommendations = {
                                                                                                                                                                                                                                                            "Critical": "Immediate remediation required. These vulnerabilities pose the highest risk.",
                                                                                                                                                                                                                                                            "High": "Prompt remediation recommended. These vulnerabilities could lead to significant impact.",
                                                                                                                                                                                                                                                            "Medium": "Address based on risk assessment. These vulnerabilities may have moderate impact.",
                                                                                                                                                                                                                                                            "Low": "Monitor and address as resources allow. These vulnerabilities have minimal impact.",
                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                        for severity, recommendation in severity_recommendations.items():
                                                                                                                                                                                                                        self.cell(
                                                                                                                                                                                                                        0, 10, f"{severity}: {recommendation}", 0, 1)

                                                                                                                                                                                                                        self.ln(
                                                                                                                                                                                                                        10)

                                                                                                                                                                                                                            def add_technical_details(self, _findings):
                                                                                                                                                                                                                            """Add technical details section.

                                                                                                                                                                                                                                                                        Args:
                                                                                                                                                                                                                                                                        findings (list): List of scan findings.
                                                                                                                                                                                                                                                                        """
                                                                                                                                                                                                                                                                        self.set_font(
                                                                                                                                                                                                                                                                        "Arial", "B", 14)
                                                                                                                                                                                                                                                                        self.cell(
                                                                                                                                                                                                                                                                        0, 10, "Technical Details", 0, 1)
                                                                                                                                                                                                                                                                        self.set_font(
                                                                                                                                                                                                                                                                        "Arial", "", 12)

                                                                                                                                                                                                                                                                        # Group findings by target
                                                                                                                                                                                                                                                                        target_findings = defaultdict(
                                                                                                                                                                                                                                                                        list)
                                                                                                                                                                                                                                for finding in findings:
                                                                                                                                                                                                                                target_findings[finding.get(
                                                                                                                                                                                                                                "target", "Unknown")].append(finding)

                                                                                                                                                                                                                                    for target, findings in target_findings.items():
                                                                                                                                                                                                                                    self.set_font(
                                                                                                                                                                                                                                    "Arial", "B", 12)
                                                                                                                                                                                                                                    self.cell(
                                                                                                                                                                                                                                    0, 10, f"Target: {target}", 0, 1)
                                                                                                                                                                                                                                    self.set_font(
                                                                                                                                                                                                                                    "Arial", "", 12)

                                                                                                                                                                                                                                        for finding in findings:
                                                                                                                                                                                                                                        severity = finding.get(
                                                                                                                                                                                                                                        "severity", "").lower()
                                                                                                                                                                                                                                        color = self.colors.get(
                                                                                                                                                                                                                                        severity, (0, 0, 0))
                                                                                                                                                                                                                                        self.set_text_color(
                                                                                                                                                                                                                                        *color)

                                                                                                                                                                                                                                        self.cell(
                                                                                                                                                                                                                                        0, 10, f"Vulnerability: {finding.get('vulnerability', '')}", 0, 1
                                                                                                                                                                                                                                        )
                                                                                                                                                                                                                                        self.cell(
                                                                                                                                                                                                                                        0, 10, f"Severity: {finding.get('severity', '')}", 0, 1)
                                                                                                                                                                                                                                        self.multi_cell(
                                                                                                                                                                                                                                        0, 10, f"Details: {finding.get('details', '')}")
                                                                                                                                                                                                                                        self.ln(
                                                                                                                                                                                                                                        5)
                                                                                                                                                                                                                                        self.set_text_color(
                                                                                                                                                                                                                                        0, 0, 0)

                                                                                                                                                                                                                                        self.ln(
                                                                                                                                                                                                                                        10)

                                                                                                                                                                                                                                            def add_appendix(self, _findings):
                                                                                                                                                                                                                                            """Add appendix section.

                                                                                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                                                                                            findings (list): List of scan findings.
                                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                            "Arial", "B", 14)
                                                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                                                            0, 10, "Appendix", 0, 1)
                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                                                                            # Add risk assessment matrix
                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                            "Arial", "B", 12)
                                                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                                                            0, 10, "Risk Assessment Matrix:", 0, 1)
                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                                                                            risk_matrix = {
                                                                                                                                                                                                                                                                                            "Critical": "Immediate action required",
                                                                                                                                                                                                                                                                                            "High": "Action required within 7 days",
                                                                                                                                                                                                                                                                                            "Medium": "Action required within 30 days",
                                                                                                                                                                                                                                                                                            "Low": "Monitor and address as needed",
                                                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                                                for severity, action in risk_matrix.items():
                                                                                                                                                                                                                                                self.cell(
                                                                                                                                                                                                                                                0, 10, f"{severity}: {action}", 0, 1)

                                                                                                                                                                                                                                                self.ln(
                                                                                                                                                                                                                                                10)

                                                                                                                                                                                                                                                # Add references and resources
                                                                                                                                                                                                                                                self.set_font(
                                                                                                                                                                                                                                                "Arial", "B", 12)
                                                                                                                                                                                                                                                self.cell(
                                                                                                                                                                                                                                                0, 10, "References and Resources:", 0, 1)
                                                                                                                                                                                                                                                self.set_font(
                                                                                                                                                                                                                                                "Arial", "", 12)

                                                                                                                                                                                                                                                resources = [
                                                                                                                                                                                                                                                "OWASP Top Ten Project",
                                                                                                                                                                                                                                                "NIST Cybersecurity Framework",
                                                                                                                                                                                                                                                "CIS Critical Security Controls",
                                                                                                                                                                                                                                                "MITRE ATT&CK Framework",
                                                                                                                                                                                                                                                ]

                                                                                                                                                                                                                                                    for resource in resources:
                                                                                                                                                                                                                                                    self.cell(
                                                                                                                                                                                                                                                    0, 10, f"- {resource}", 0, 1)

                                                                                                                                                                                                                                                    self.ln(
                                                                                                                                                                                                                                                    10)

                                                                                                                                                                                                                                                        def add_findings(self, _findings):
                                                                                                                                                                                                                                                        """Add findings to the report.

                                                                                                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                                                                                                            findings (list): List of scan findings.
                                                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                                            "Arial", "B", 14)
                                                                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                                                                            0, 10, "Findings", 0, 1)
                                                                                                                                                                                                                                                                                                            self.set_font(
                                                                                                                                                                                                                                                                                                            "Arial", "", 12)

                                                                                                                                                                                                                                                            for finding in findings:
                                                                                                                                                                                                                                                            severity = finding.get(
                                                                                                                                                                                                                                                            "severity", "").lower()
                                                                                                                                                                                                                                                            color = self.colors.get(
                                                                                                                                                                                                                                                            severity, (0, 0, 0))
                                                                                                                                                                                                                                                            self.set_text_color(
                                                                                                                                                                                                                                                            *color)

                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                            0, 10, f"Target: {finding.get('target', '')}", 0, 1)
                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                            0, 10, f"Vulnerability: {finding.get('vulnerability', '')}", 0, 1)
                                                                                                                                                                                                                                                            self.cell(
                                                                                                                                                                                                                                                            0, 10, f"Severity: {finding.get('severity', '')}", 0, 1)
                                                                                                                                                                                                                                                            self.multi_cell(
                                                                                                                                                                                                                                                            0, 10, f"Details: {finding.get('details', '')}")
                                                                                                                                                                                                                                                            self.ln(
                                                                                                                                                                                                                                                            5)
                                                                                                                                                                                                                                                            self.set_text_color(
                                                                                                                                                                                                                                                            0, 0, 0)