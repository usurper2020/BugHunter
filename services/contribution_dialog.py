from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QTextEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime

class ContributionDialog(QDialog):
    """Dialog for managing user contributions"""
    
    contribution_submitted = pyqtSignal()  # Signal emitted when a contribution is submitted
    
    def __init__(self, contribution_system, current_user, parent=None):
        super().__init__(parent)
        self.contribution_system = contribution_system
        self.current_user = current_user
        self.setup_ui()
        self.load_contributions()
        
    def setup_ui(self):
        """Set up the contribution dialog UI"""
        self.setWindowTitle("Contributions")
        self.setModal(False)  # Allow interaction with main window
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Contributions list
        list_section = QVBoxLayout()
        list_section.addWidget(QLabel("Your Contributions"))
        
        self.contributions_table = QTableWidget()
        self.contributions_table.setColumnCount(5)
        self.contributions_table.setHorizontalHeaderLabels([
            "Type", "Status", "Points", "Submitted", "Actions"
        ])
        self.contributions_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        list_section.addWidget(self.contributions_table)
        layout.addLayout(list_section)
        
        # Submit new contribution section
        submit_section = QVBoxLayout()
        submit_section.addWidget(QLabel("Submit New Contribution"))
        
        # Contribution type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "vulnerability", "fix", "documentation", "feedback"
        ])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        submit_section.addLayout(type_layout)
        
        # For vulnerability type
        self.vuln_section = QVBoxLayout()
        
        severity_layout = QHBoxLayout()
        severity_label = QLabel("Severity:")
        self.severity_combo = QComboBox()
        self.severity_combo.addItems([
            "critical", "high", "medium", "low"
        ])
        severity_layout.addWidget(severity_label)
        severity_layout.addWidget(self.severity_combo)
        self.vuln_section.addLayout(severity_layout)
        
        submit_section.addLayout(self.vuln_section)
        self.vuln_section.setVisible(False)
        
        # Title field
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        submit_section.addLayout(title_layout)
        
        # Description field
        description_layout = QVBoxLayout()
        description_label = QLabel("Description:")
        self.description_input = QTextEdit()
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_input)
        submit_section.addLayout(description_layout)
        
        # Tags field
        tags_layout = QHBoxLayout()
        tags_label = QLabel("Tags:")
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Comma-separated tags")
        tags_layout.addWidget(tags_label)
        tags_layout.addWidget(self.tags_input)
        submit_section.addLayout(tags_layout)
        
        # Submit button
        self.submit_button = QPushButton("Submit Contribution")
        submit_section.addWidget(self.submit_button)
        
        layout.addLayout(submit_section)
        
        # Connect signals
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.submit_button.clicked.connect(self.submit_contribution)
        
        # Set style
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: none;
                border-right: 1px solid #cccccc;
            }
        """)
        
    def load_contributions(self):
        """Load user's contributions"""
        result = self.contribution_system.get_user_contributions(self.current_user)
        if result["status"] == "success":
            self.contributions_table.setRowCount(0)
            for contribution in result["contributions"]:
                row = self.contributions_table.rowCount()
                self.contributions_table.insertRow(row)
                
                self.contributions_table.setItem(
                    row, 0, QTableWidgetItem(contribution["type"])
                )
                self.contributions_table.setItem(
                    row, 1, QTableWidgetItem(contribution["status"])
                )
                self.contributions_table.setItem(
                    row, 2, QTableWidgetItem(str(contribution["points"]))
                )
                self.contributions_table.setItem(
                    row, 3, QTableWidgetItem(contribution["submitted_at"])
                )
                
                # Add view button
                view_button = QPushButton("View")
                view_button.clicked.connect(
                    lambda c, contrib=contribution: self.view_contribution(contrib)
                )
                self.contributions_table.setCellWidget(row, 4, view_button)
                
    def on_type_changed(self, contribution_type: str):
        """Handle contribution type change"""
        self.vuln_section.setVisible(contribution_type == "vulnerability")
        
    def submit_contribution(self):
        """Submit a new contribution"""
        contribution_type = self.type_combo.currentText()
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        
        if not title or not description:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please fill in all required fields."
            )
            return
            
        content = {
            "title": title,
            "description": description
        }
        
        if contribution_type == "vulnerability":
            content["severity"] = self.severity_combo.currentText()
            
        result = self.contribution_system.submit_contribution(
            user=self.current_user,
            contribution_type=contribution_type,
            content=content,
            tags=tags
        )
        
        if result["status"] == "success":
            QMessageBox.information(
                self,
                "Success",
                "Contribution submitted successfully."
            )
            self.title_input.clear()
            self.description_input.clear()
            self.tags_input.clear()
            self.load_contributions()
            self.contribution_submitted.emit()
        else:
            QMessageBox.warning(
                self,
                "Error",
                result.get("message", "Failed to submit contribution.")
            )
            
    def view_contribution(self, contribution: dict):
        """View contribution details"""
        # TODO: Implement contribution viewing dialog
        QMessageBox.information(
            self,
            "Contribution Details",
            f"Type: {contribution['type']}\n"
            f"Status: {contribution['status']}\n"
            f"Points: {contribution['points']}\n"
            f"Submitted: {contribution['submitted_at']}\n\n"
            f"Title: {contribution['content']['title']}\n"
            f"Description: {contribution['content']['description']}"
        )
