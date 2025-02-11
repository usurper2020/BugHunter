# tabs/nuclei_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QComboBox
)

class NucleiTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Target input
        target_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        target_layout.addWidget(QLabel("Target:"))
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)
        
        # Template selection
        template_layout = QHBoxLayout()
        self.template_combo = QComboBox()
        self.template_combo.addItems(['All', 'CVEs', 'Vulnerabilities', 'Misconfigurations'])
        template_layout.addWidget(QLabel("Template:"))
        template_layout.addWidget(self.template_combo)
        layout.addLayout(template_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
