"""
Nuclei scanner interface tab for the BugHunter application.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QComboBox, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt
from services.vulnerability_scanner import VulnerabilityScanner
from Nuclei.nuclei_analyzer import Nuclei_analyzer
from models.scan_target import ScanTarget
import requests

class NucleiTab(QWidget):
    """Tab widget for Nuclei vulnerability scanner."""
    
    def __init__(self, scanner: VulnerabilityScanner, analyzer: Nuclei_analyzer = None):
        """Initialize the Nuclei scanner interface."""
        super().__init__()
        self.scanner = scanner
        self.analyzer = analyzer or Nuclei_analyzer()
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components."""
        layout = QVBoxLayout()
        
        # Target section
        target_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target URL")
        target_layout.addWidget(QLabel("Target:"))
        target_layout.addWidget(self.target_input)
        self.analyze_button = QPushButton("Analyze Target")
        self.analyze_button.clicked.connect(self.analyze_target)
        target_layout.addWidget(self.analyze_button)
        layout.addLayout(target_layout)
        
        # Template search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search templates (e.g., 'wordpress', 'sql-injection')")
        self.search_input.textChanged.connect(self.search_templates)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Filters section
        filter_layout = QHBoxLayout()
        
        # Category filter
        self.category_combo = QComboBox()
        self.category_combo.addItems(['All Categories', 'CVEs', 'Vulnerabilities', 'Misconfigurations', 'Exposures', 'Technologies'])
        self.category_combo.currentTextChanged.connect(self.search_templates)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_combo)
        
        # Severity filter
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(['All Severities', 'Critical', 'High', 'Medium', 'Low', 'Info'])
        self.severity_combo.currentTextChanged.connect(self.search_templates)
        filter_layout.addWidget(QLabel("Severity:"))
        filter_layout.addWidget(self.severity_combo)
        
        layout.addLayout(filter_layout)
        
        # Template results table
        self.templates_table = QTableWidget()
        self.templates_table.setColumnCount(5)
        self.templates_table.setHorizontalHeaderLabels(["ID", "Category", "Severity", "Description", "Select"])
        header = self.templates_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.templates_table)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Scan")
        self.stop_button = QPushButton("Stop Scan")
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Results section
        layout.addWidget(QLabel("Scan Results:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        # AI Analysis section
        layout.addWidget(QLabel("AI Analysis:"))
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        layout.addWidget(self.ai_output)
        
        self.setLayout(layout)
        
        # Initial template search
        self.search_templates()

    def search_templates(self):
        """Search and display templates based on current filters."""
        query = self.search_input.text()
        category = self.category_combo.currentText()
        severity = self.severity_combo.currentText()
        
        # Adjust category and severity if "All" is selected
        category = None if category == 'All Categories' else category
        severity = None if severity == 'All Severities' else severity.lower()
        
        # Search templates
        results = self.analyzer.search_templates(query, category, severity)
        
        # Update table
        self.templates_table.setRowCount(len(results))
        for row, template in enumerate(results):
            # Template ID
            id_item = QTableWidgetItem(template['id'])
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.templates_table.setItem(row, 0, id_item)
            
            # Category
            cat_item = QTableWidgetItem(template['category'])
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.templates_table.setItem(row, 1, cat_item)
            
            # Severity
            sev_item = QTableWidgetItem(template['severity'])
            sev_item.setFlags(sev_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.templates_table.setItem(row, 2, sev_item)
            
            # Description
            desc_item = QTableWidgetItem(template['description'])
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.templates_table.setItem(row, 3, desc_item)
            
            # Checkbox for selection
            checkbox = QCheckBox()
            self.templates_table.setCellWidget(row, 4, checkbox)

    def analyze_target(self):
        """Analyze target website and suggest relevant templates."""
        url = self.target_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL.")
            return
            
        try:
            # Create scan target
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            target = ScanTarget(url)
            
            # Fetch website content
            response = requests.get(target.url)
            content = response.text
            
            # Analyze content against templates
            matches = self.analyzer.analyze_website_content(target.url, content)
            
            # Update AI analysis output
            self.ai_output.clear()
            if matches:
                self.ai_output.append("🔍 AI Analysis Results:\n")
                for match in matches:
                    self.ai_output.append(f"• Potential {match['severity']} severity issue detected:")
                    self.ai_output.append(f"  - Category: {match['category']}")
                    self.ai_output.append(f"  - Description: {match['description']}")
                    self.ai_output.append(f"  - Confidence: {match['confidence']}\n")
                    
                    # Auto-select relevant templates
                    for row in range(self.templates_table.rowCount()):
                        if self.templates_table.item(row, 0).text() == match['template_id']:
                            checkbox = self.templates_table.cellWidget(row, 4)
                            checkbox.setChecked(True)
            else:
                self.ai_output.append("No immediate potential vulnerabilities detected.")
                
        except Exception as e:
            QMessageBox.warning(self, "Analysis Error", f"Error analyzing target: {str(e)}")

    def start_scan(self):
        """Start Nuclei scan with selected templates."""
        url = self.target_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL.")
            return
            
        # Create scan target
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        target = ScanTarget(url)
            
        # Get selected templates
        selected_templates = []
        for row in range(self.templates_table.rowCount()):
            checkbox = self.templates_table.cellWidget(row, 4)
            if checkbox.isChecked():
                template_id = self.templates_table.item(row, 0).text()
                template = self.analyzer.get_template_details(template_id)
                if template:
                    selected_templates.append(template['path'])
        
        if not selected_templates:
            QMessageBox.warning(self, "Selection Error", "Please select at least one template.")
            return
            
        # Start scan
        self.output_text.clear()
        self.output_text.append(f"Starting scan on {target.url} with {len(selected_templates)} templates...")
        
        # Run the scan
        scan_result = self.scanner.run_scan(target)
        if scan_result['status'] == 'success':
            self.output_text.append("\nScan completed successfully!")
            self.output_text.append("\nFindings:")
            for finding in scan_result['results']['findings']:
                self.output_text.append(f"\n• {finding['type']} ({finding['severity']} severity)")
                self.output_text.append(f"  Description: {finding['description']}")
                self.output_text.append(f"  Details: {finding['details']}")
        else:
            self.output_text.append(f"\nScan failed: {scan_result['message']}")

    def stop_scan(self):
        """Stop the currently running scan."""
        self.output_text.append("Stopping scan...")
        # TODO: Implement actual scan stopping logic
