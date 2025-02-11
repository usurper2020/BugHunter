from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class BugBountyTargetTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Target Website:"))
        self.target_input = QLineEdit()
        layout.addWidget(self.target_input)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_target)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def submit_target(self):
        target_website = self.target_input.text()
        # Here you would add the logic to process the target website
        print(f"Target website submitted: {target_website}")  # Placeholder for processing logic
        self.target_input.clear()  # Clear the input box after submission
