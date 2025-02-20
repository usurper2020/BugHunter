"""
Report Generator Module.

This module provides the report generation interface for BugHunter,
handling scan results and generating various report formats.

Classes:
    ReportGeneratorTab: Report generator tab class.
    PDFReport: Custom PDF report class.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QFileDialog, QMessageBox,
    QLineEdit, QColorDialog
)
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtGui import QColor
import json
import csv
from fpdf import FPDF
from collections import defaultdict

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

    report_generated = pyqtSignal(str)

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
        meta_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter report title")
        meta_layout.addWidget(self.title_input)
        
        meta_layout.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        meta_layout.addWidget(self.author_input)
        layout.addLayout(meta_layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(
            ["Target", "Vulnerability", "Severity", "Details"]
        )
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.results_table)

        # Export controls
        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Export Format:"))
        
        self.export_combo = QComboBox()
        self.export_combo.addItems(["JSON", "CSV", "PDF"])
        export_layout.addWidget(self.export_combo)
        
        export_layout.addWidget(QLabel("Template:"))
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Basic", "Detailed", "Executive", "Technical"])
        export_layout.addWidget(self.template_combo)
        
        self.style_button = QPushButton("Customize Style")
        export_layout.addWidget(self.style_button)
        
        self.export_button = QPushButton("Export Report")
        export_layout.addWidget(self.export_button)
        
        layout.addLayout(export_layout)
        self.setLayout(layout)

    def connect_signals(self):
        """Connect UI signals to appropriate slots."""
        self.export_button.clicked.connect(self.export_report)
        self.style_button.clicked.connect(self.customize_style)

    def add_scan_result(self, result):
        """Add a scan result to the report.
        
        Args:
            result (dict): Scan result to add.
        """
        self.scan_results.append(result)
        self.update_results_table()

    def update_results_table(self):
        """Update the results table with current scan results."""
        self.results_table.setRowCount(len(self.scan_results))
        
        for row, result in enumerate(self.scan_results):
            self.results_table.setItem(row, 0, QTableWidgetItem(result.get('target', '')))
            self.results_table.setItem(row, 1, QTableWidgetItem(result.get('vulnerability', '')))
            self.results_table.setItem(row, 2, QTableWidgetItem(result.get('severity', '')))
            self.results_table.setItem(row, 3, QTableWidgetItem(result.get('details', '')))

    def export_report(self):
        """Export the report in the selected format."""
        export_format = self.export_combo.currentText()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "", f"{export_format} Files (*.{export_format.lower()})"
        )
        
        if file_path:
            try:
                if export_format == "JSON":
                    self.export_json(file_path)
                elif export_format == "CSV":
                    self.export_csv(file_path)
                elif export_format == "PDF":
                    self.export_pdf(file_path)
                
                self.report_generated.emit(f"Report successfully exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export report: {str(e)}")

    def customize_style(self):
        """Open style customization dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.apply_style(color)

    def apply_style(self, color):
        """Apply custom style to the report.
        
        Args:
            color (QColor): Selected color for styling.
        """
        # TODO: Implement style application
        pass

    def export_json(self, file_path):
        """Export report as JSON.
        
        Args:
            file_path (str): Path to save the JSON file.
        """
        report_data = self.get_report_metadata()
        report_data['findings'] = self.scan_results
        
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=4)

    def export_csv(self, file_path):
        """Export report as CSV.
        
        Args:
            file_path (str): Path to save the CSV file.
        """
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["target", "vulnerability", "severity", "details"])
            writer.writeheader()
            writer.writerows(self.scan_results)

    def export_pdf(self, file_path):
        """Export report as PDF.
        
        Args:
            file_path (str): Path to save the PDF file.
        """
        template = self.template_combo.currentText()
        pdf = PDFReport(template)
        pdf.set_metadata(**self.get_report_metadata())
        
        if template == "Executive":
            pdf.add_executive_summary(self.scan_results)
            pdf.add_recommendations(self.scan_results)
        elif template == "Technical":
            pdf.add_technical_details(self.scan_results)
            pdf.add_appendix(self.scan_results)
        else:
            pdf.add_findings(self.scan_results)
            
        pdf.output(file_path)

    def get_report_metadata(self):
        """Get report metadata.
        
        Returns:
            dict: Dictionary containing report metadata.
        """
        return {
            'title': self.title_input.text() or "BugHunter Report",
            'author': self.author_input.text() or "BugHunter",
            'date': QDate.currentDate().toString("yyyy-MM-dd")
        }

    def cleanup(self):
        """Clean up resources before closing."""
        self.scan_results.clear()
        self.results_table.setRowCount(0)

class PDFReport(FPDF):
    """Custom PDF report class."""
    
    def __init__(self, template="Basic"):
        """Initialize the PDF report.
        
        Args:
            template (str): Template to use for the report.
        """
        super().__init__()
        self.template = template
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font('Arial', '', 12)
        self.colors = {
            'header': (0, 51, 102),
            'critical': (255, 0, 0),
            'high': (255, 128, 0),
            'medium': (255, 255, 0),
            'low': (0, 128, 0)
        }

    def header(self):
        """Add header to each page."""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(*self.colors['header'])
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Author: {self.author} | Date: {self.date}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_executive_summary(self, findings):
        """Add executive summary section.
        
        Args:
            findings (list): List of scan findings.
        """
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Executive Summary", 0, 1)
        self.set_font('Arial', '', 12)
        
        # Calculate statistics
        severity_counts = defaultdict(int)
        for finding in findings:
            severity_counts[finding.get('severity', 'Unknown')] += 1
        
        # Add summary content
        self.multi_cell(0, 10, 
            f"This report summarizes the findings from the security scan conducted on {self.date}. "
            "The following key metrics were identified:"
        )
        self.ln(5)
        
        for severity, count in severity_counts.items():
            self.cell(0, 10, f"- {severity} severity findings: {count}", 0, 1)
        
        self.ln(10)

    def add_recommendations(self, findings):
        """Add recommendations section.
        
        Args:
            findings (list): List of scan findings.
        """
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Recommendations", 0, 1)
        self.set_font('Arial', '', 12)
        
        # Add general recommendations
        self.multi_cell(0, 10,
            "Based on the findings, the following recommendations are proposed:\n"
            "1. Address critical and high severity findings immediately\n"
            "2. Review medium severity findings for potential risks\n"
            "3. Monitor low severity findings for future improvements\n"
            "4. Implement regular security audits\n"
            "5. Establish a vulnerability management process"
        )
        self.ln(10)
        
        # Add specific recommendations by severity
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Detailed Recommendations by Severity:", 0, 1)
        self.set_font('Arial', '', 12)
        
        severity_recommendations = {
            'Critical': "Immediate remediation required. These vulnerabilities pose the highest risk.",
            'High': "Prompt remediation recommended. These vulnerabilities could lead to significant impact.",
            'Medium': "Address based on risk assessment. These vulnerabilities may have moderate impact.",
            'Low': "Monitor and address as resources allow. These vulnerabilities have minimal impact."
        }
        
        for severity, recommendation in severity_recommendations.items():
            self.cell(0, 10, f"{severity}: {recommendation}", 0, 1)
        
        self.ln(10)

    def add_technical_details(self, findings):
        """Add technical details section.
        
        Args:
            findings (list): List of scan findings.
        """
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Technical Details", 0, 1)
        self.set_font('Arial', '', 12)
        
        # Group findings by target
        target_findings = defaultdict(list)
        for finding in findings:
            target_findings[finding.get('target', 'Unknown')].append(finding)
        
        for target, findings in target_findings.items():
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, f"Target: {target}", 0, 1)
            self.set_font('Arial', '', 12)
            
            for finding in findings:
                severity = finding.get('severity', '').lower()
                color = self.colors.get(severity, (0, 0, 0))
                self.set_text_color(*color)
                
                self.cell(0, 10, f"Vulnerability: {finding.get('vulnerability', '')}", 0, 1)
                self.cell(0, 10, f"Severity: {finding.get('severity', '')}", 0, 1)
                self.multi_cell(0, 10, f"Details: {finding.get('details', '')}")
                self.ln(5)
                self.set_text_color(0, 0, 0)
            
            self.ln(10)

    def add_appendix(self, findings):
        """Add appendix section.
        
        Args:
            findings (list): List of scan findings.
        """
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Appendix", 0, 1)
        self.set_font('Arial', '', 12)
        
        # Add risk assessment matrix
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Risk Assessment Matrix:", 0, 1)
        self.set_font('Arial', '', 12)
        
        risk_matrix = {
            'Critical': "Immediate action required",
            'High': "Action required within 7 days",
            'Medium': "Action required within 30 days",
            'Low': "Monitor and address as needed"
        }
        
        for severity, action in risk_matrix.items():
            self.cell(0, 10, f"{severity}: {action}", 0, 1)
        
        self.ln(10)
        
        # Add references and resources
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "References and Resources:", 0, 1)
        self.set_font('Arial', '', 12)
        
        resources = [
            "OWASP Top Ten Project",
            "NIST Cybersecurity Framework",
            "CIS Critical Security Controls",
            "MITRE ATT&CK Framework"
        ]
        
        for resource in resources:
            self.cell(0, 10, f"- {resource}", 0, 1)
        
        self.ln(10)

    def add_findings(self, findings):
        """Add findings to the report.
        
        Args:
            findings (list): List of scan findings.
        """
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Findings", 0, 1)
        self.set_font('Arial', '', 12)
        
        for finding in findings:
            severity = finding.get('severity', '').lower()
            color = self.colors.get(severity, (0, 0, 0))
            self.set_text_color(*color)
            
            self.cell(0, 10, f"Target: {finding.get('target', '')}", 0, 1)
            self.cell(0, 10, f"Vulnerability: {finding.get('vulnerability', '')}", 0, 1)
            self.cell(0, 10, f"Severity: {finding.get('severity', '')}", 0, 1)
            self.multi_cell(0, 10, f"Details: {finding.get('details', '')}")
            self.ln(5)
            self.set_text_color(0, 0, 0)
