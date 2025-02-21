from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QComboBox, QMessageBox)

class ContributionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contribution")
        self.setMinimumSize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout()
        
        # Contribution type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Bug Report", "Feature Request", "Documentation", "Other"])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Content area
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Enter contribution details...")
        layout.addWidget(self.content_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_contribution)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def submit_contribution(self):
        """Handle contribution submission"""
        content = self.content_edit.toPlainText()
        if not content:
            QMessageBox.warning(self, "Error", "Please enter contribution details")
            return
            
        contribution_data = {
            'type': self.type_combo.currentText(),
            'content': content
        }
        
        # Here you would typically send the contribution to the contribution system
        self.accept()
        
    def show(self):
        """Show the dialog"""
        return self.exec()
