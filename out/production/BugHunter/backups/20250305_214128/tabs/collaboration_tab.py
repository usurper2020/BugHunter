from services.collaboration_system import CollaborationSystem
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

status = "active"
k = 10
message = ""
tools = []
"""
Collaboration tab for the BugHunter application.

This tab provides tools for team collaboration with real-time status updates
and progress tracking.
"""


class CollaborationTab(QWidget):
    """
    Tab widget providing comprehensive team collaboration functionality.

        Features:
        - Real-time chat
        - Task management
        - File sharing
        - Progress tracking
        - Interactive controls
    """

    def __init__(self):
        super().__init__()
        self.collab_system = CollaborationSystem()
        self.init_ui()
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)

        def init_ui(self):
            """Initialize the UI components with enhanced status tracking."""
            main_layout = QVBoxLayout()

            # Create a splitter for better layout management
            splitter = QSplitter()
            splitter.set_orientation(
                Qt.Orientation.Vertical
            )  # Corrected: Use Qt.Orientation enum

            # Top panel - Chat and collaboration
            top_panel = QWidget()
            top_layout = QVBoxLayout(top_panel)

            # Online users list
            self.user_list = QListWidget()
            top_layout.add_widget(QLabel("Online Users:"))
            top_layout.add_widget(self.user_list)

            # Chat window
            self.chat_window = QTextEdit()
            self.chat_window.set_read_only(True)
            top_layout.add_widget(QLabel("Chat:"))
            top_layout.add_widget(self.chat_window)

            # Chat input
            self.chat_input = QLineEdit()
            self.chat_input.set_placeholder_text("Type your message...")
            self.chat_input.return_pressed.connect(self.send_message)
            top_layout.add_widget(self.chat_input)

            # Bottom panel - Tasks and status
            bottom_panel = QWidget()
            bottom_layout = QVBoxLayout(bottom_panel)

            # Task list
            self.task_list = QListWidget()
            bottom_layout.add_widget(QLabel("Tasks:"))
            bottom_layout.add_widget(self.task_list)

            # Task controls
            task_controls = QHBoxLayout()
            self.new_task_input = QLineEdit()
            self.new_task_input.set_placeholder_text("New task description...")
            self.add_task_button = QPushButton("Add Task")
            self.add_task_button.clicked.connect(self.add_task)
            task_controls.add_widget(self.new_task_input)
            task_controls.add_widget(self.add_task_button)
            bottom_layout.add_layout(task_controls)

            # Status window
            self.status_window = QTextEdit()
            self.status_window.set_read_only(True)
            self.status_window.set_placeholder_text(
                "Collaboration status will appear here..."
            )
            bottom_layout.add_widget(QLabel("Status:"))
            bottom_layout.add_widget(self.status_window)

            # Add panels to splitter
            splitter.add_widget(top_panel)
            splitter.add_widget(bottom_panel)

            main_layout.add_widget(splitter)
            self.set_layout(main_layout)

            def send_message(self):
                """Send a chat message."""
                message = self.chat_input.text().strip()
                if message:
                    self.collab_system.send_message(message)
                    self.chat_input.clear()

                    def add_task(self):
                        """Add a new task to the collaboration system."""
                        task = self.new_task_input.text().strip()
                        if task:
                            self.collab_system.add_task(task)
                            self.new_task_input.clear()

                            def update_status(self):
                                """Update the status window with current collaboration information."""
                                # Update online users
                                self.user_list.clear()
                                users = self.collab_system.get_online_users()
                                self.user_list.add_items(users)

                                # Update chat messages
                                messages = self.collab_system.get_messages()
                                self.chat_window.clear()
                                self.chat_window.append("\n".join(messages))

                                # Update tasks
                                self.task_list.clear()
                                tasks = self.collab_system.get_tasks()
                                self.task_list.add_items(tasks)

                                # Update status messages
                                status = self.collab_system.get_status()
                                self.status_window.append(status)

                                def start_collaboration(self):
                                    """Start the collaboration session."""
                                    self.status_timer.start(1000)
                                    self.status_window.append(
                                        "Collaboration session started"
                                    )

                                    def stop_collaboration(self):
                                        """Stop the collaboration session."""
                                        self.status_timer.stop()
                                        self.status_window.append(
                                            "Collaboration session stopped"
                                        )
