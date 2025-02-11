from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox
)
from services.tool_manager import ToolManager

class ToolManagerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.tool_manager = ToolManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Tool URL input
        url_layout = QHBoxLayout()
        self.tool_url_input = QLineEdit()
        self.tool_url_input.setPlaceholderText("Enter GitHub tool URL")
        url_layout.addWidget(QLabel("Tool URL:"))
        url_layout.addWidget(self.tool_url_input)
        layout.addLayout(url_layout)

        # Download button
        self.download_button = QPushButton("Download Tool")
        self.download_button.clicked.connect(self.download_tool)
        layout.addWidget(self.download_button)

        # Dropdown for downloaded tools
        self.tool_dropdown = QComboBox()
        layout.addWidget(QLabel("Downloaded Tools:"))
        layout.addWidget(self.tool_dropdown)

        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def download_tool(self):
        """Download the tool from the provided GitHub URL"""
        tool_url = self.tool_url_input.text().strip()
        if not tool_url:
            QMessageBox.warning(self, "Input Error", "Please enter a valid GitHub tool URL.")
            return

        try:
            result = self.tool_manager.install_github_tool(tool_url, 'main.py')  # Assuming 'main.py' is the main file
            if result['status'] == 'success':
                self.output_text.append(result['message'])
                self.tool_dropdown.addItem(os.path.basename(tool_url))
            else:
                QMessageBox.warning(self, "Download Error", result['message'])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
