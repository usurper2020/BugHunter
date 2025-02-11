from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar


class TrainingUI(QWidget):
    """
    GUI for AI Model Training functionality.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Training")
        self.layout = QVBoxLayout()

        # Status Label
        self.status_label = QLabel("AI Model Training Status: Idle")
        self.layout.addWidget(self.status_label)

        # Start Training Button
        self.start_button = QPushButton("Start Training")
        self.layout.addWidget(self.start_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
        self.start_button.clicked.connect(self.start_training)

    def start_training(self):
        # Simulated training logic
        self.status_label.setText("AI Model Training Status: In Progress...")
        self.progress_bar.setValue(50)  # Update with simulated progress
        # Simulating completion
        self.progress_bar.setValue(100)
        self.status_label.setText("AI Model Training Status: Completed!")
