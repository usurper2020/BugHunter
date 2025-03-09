from services.vulnerability_scanner import VulnerabilityScanner
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

vulnerabilities = []
k = 10
"""
Bug Bounty Target tab for the BugHunter application.

This tab provides an interface for managing bug bounty targets,
including adding, removing, and scanning targets.
"""


class BugBountyTargetTab(QWidget):
    """
    Tab widget for managing bug bounty targets.

        This widget provides:
        - Input field for adding new targets
        - List of current targets
        - Buttons for managing targets
        - Integration with the vulnerability scanner
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanner = VulnerabilityScanner()

        def init_ui(self):
            """Initialize the UI components."""
            layout = QVBoxLayout()

            # Target input
            self.target_input = QLineEdit()
            self.target_input.set_placeholder_text(
                "Enter target URL or IP address")
            layout.add_widget(self.target_input)

            # Add target button
            add_button = QPushButton("Add Target")
            add_button.clicked.connect(self.add_target)
            layout.add_widget(add_button)

            # Target list
            self.target_list = QListWidget()
            layout.add_widget(QLabel("Current Targets:"))
            layout.add_widget(self.target_list)

            # Scan button
            scan_button = QPushButton("Scan Selected Target")
            scan_button.clicked.connect(self.scan_target)
            layout.add_widget(scan_button)

            self.set_layout(layout)

            def add_target(self):
                """Add a new target to the list."""
                target = self.target_input.text().strip()
                if target and target not in [
                    self.target_list.item(i).text()
                    for i in range(self.target_list.count())
                ]:
                    self.target_list.add_item(target)
                    self.target_input.clear()

                    def scan_target(self):
                        """Scan the selected target for vulnerabilities."""
                        selected = self.target_list.current_item()
                        if selected:
                            target = selected.text()
                            results = self.scanner.scan(target)
                            # TODO: Display scan results
