from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QMessageBox)

class CollaborationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Collaboration")
        self.setMinimumSize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout()
        
        # Report content area
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Enter report content...")
        layout.addWidget(self.content_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.share_button = QPushButton("Share")
        self.share_button.clicked.connect(self.share_report)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.share_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def share_report(self):
        """Handle report sharing"""
        content = self.content_edit.toPlainText()
        if not content:
            QMessageBox.warning(self, "Error", "Please enter report content")
            return
            
        # Here you would typically send the report to the collaboration system
        self.accept()
        
    def show(self):
        """Show the dialog"""
        return self.exec()
