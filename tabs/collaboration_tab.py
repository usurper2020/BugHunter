"""
Collaboration tab for the BugHunter application.

This tab provides tools for team collaboration with real-time status updates
and progress tracking.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton, QSplitter, QProgressBar,
                           QListWidget, QComboBox, QLineEdit)
from PyQt6.QtCore import QTimer
from services.collaboration_system import CollaborationSystem

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
        splitter.setOrientation(1)  # Vertical split
        
        # Top panel - Chat and collaboration
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        # Online users list
        self.user_list = QListWidget()
        top_layout.addWidget(QLabel("Online Users:"))
        top_layout.addWidget(self.user_list)
        
        # Chat window
        self.chat_window = QTextEdit()
        self.chat_window.setReadOnly(True)
        top_layout.addWidget(QLabel("Chat:"))
        top_layout.addWidget(self.chat_window)
        
        # Chat input
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message...")
        self.chat_input.returnPressed.connect(self.send_message)
        top_layout.addWidget(self.chat_input)
        
        # Bottom panel - Tasks and status
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # Task list
        self.task_list = QListWidget()
        bottom_layout.addWidget(QLabel("Tasks:"))
        bottom_layout.addWidget(self.task_list)
        
        # Task controls
        task_controls = QHBoxLayout()
        self.new_task_input = QLineEdit()
        self.new_task_input.setPlaceholderText("New task description...")
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        task_controls.addWidget(self.new_task_input)
        task_controls.addWidget(self.add_task_button)
        bottom_layout.addLayout(task_controls)
        
        # Status window
        self.status_window = QTextEdit()
        self.status_window.setReadOnly(True)
        self.status_window.setPlaceholderText("Collaboration status will appear here...")
        bottom_layout.addWidget(QLabel("Status:"))
        bottom_layout.addWidget(self.status_window)
        
        # Add panels to splitter
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

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
        self.user_list.addItems(users)
        
        # Update chat messages
        messages = self.collab_system.get_messages()
        self.chat_window.clear()
        self.chat_window.append("\n".join(messages))
        
        # Update tasks
        self.task_list.clear()
        tasks = self.collab_system.get_tasks()
        self.task_list.addItems(tasks)
        
        # Update status messages
        status = self.collab_system.get_status()
        self.status_window.append(status)

    def start_collaboration(self):
        """Start the collaboration session."""
        self.status_timer.start(1000)
        self.status_window.append("Collaboration session started")

    def stop_collaboration(self):
        """Stop the collaboration session."""
        self.status_timer.stop()
        self.status_window.append("Collaboration session stopped")
