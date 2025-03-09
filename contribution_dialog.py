from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QMessageBox)

class ContributionDialog(QDialog):
    def __init__(self, contribution_system, current_user, parent=None):
        super().__init__(parent)
        self.contribution_system = contribution_system
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Submit Contribution')
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Tool Name input
        self.tool_name_label = QLabel('Tool Name:')
        self.tool_name_input = QLineEdit()
        layout.addWidget(self.tool_name_label)
        layout.addWidget(self.tool_name_input)

        # Tool Description input
        self.tool_description_label = QLabel('Description:')
        self.tool_description_input = QTextEdit()
        layout.addWidget(self.tool_description_label)
        layout.addWidget(self.tool_description_input)

        # Tool File input
        self.tool_file_label = QLabel('Tool File Path:')
        self.tool_file_input = QLineEdit()
        layout.addWidget(self.tool_file_label)
        layout.addWidget(self.tool_file_input)

        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_contribution)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_contribution(self):
        """Submit the contribution"""
        tool_name = self.tool_name_input.text()
        tool_description = self.tool_description_input.toPlainText()
        tool_file = self.tool_file_input.text()

        if not tool_name or not tool_description or not tool_file:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        result = self.contribution_system.submit_contribution(
            self.current_user, tool_name, tool_description, tool_file)
        
        if result['status'] == 'success':
            QMessageBox.information(self, 'Success', 'Contribution submitted successfully')
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result['message'])
