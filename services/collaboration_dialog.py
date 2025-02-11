from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QTextEdit,
    QListWidget, QSplitter, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime

class CollaborationDialog(QDialog):
    """Dialog for collaboration features"""
    
    message_sent = pyqtSignal(str)  # Signal emitted when a message is sent
    
    def __init__(self, collaboration_system, current_user, parent=None):
        super().__init__(parent)
        self.collaboration_system = collaboration_system
        self.current_user = current_user
        self.current_project = None
        self.setup_ui()
        self.load_projects()
        
    def setup_ui(self):
        """Set up the collaboration dialog UI"""
        self.setWindowTitle("Collaboration")
        self.setModal(False)  # Allow interaction with main window
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create splitter for projects and chat
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Projects
        projects_widget = QWidget()
        projects_layout = QVBoxLayout()
        projects_widget.setLayout(projects_layout)
        
        # Projects list
        projects_layout.addWidget(QLabel("Projects"))
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.project_selected)
        projects_layout.addWidget(self.projects_list)
        
        # Create project section
        create_project_layout = QVBoxLayout()
        create_project_layout.addWidget(QLabel("Create New Project"))
        
        # Project name field
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Project Name")
        create_project_layout.addWidget(self.project_name_input)
        
        # Project description field
        self.project_desc_input = QTextEdit()
        self.project_desc_input.setPlaceholderText("Project Description")
        self.project_desc_input.setMaximumHeight(100)
        create_project_layout.addWidget(self.project_desc_input)
        
        # Create project button
        self.create_project_btn = QPushButton("Create Project")
        self.create_project_btn.clicked.connect(self.create_project)
        create_project_layout.addWidget(self.create_project_btn)
        
        projects_layout.addLayout(create_project_layout)
        splitter.addWidget(projects_widget)
        
        # Right side - Chat
        chat_widget = QWidget()
        chat_layout = QVBoxLayout()
        chat_widget.setLayout(chat_layout)
        
        # Chat header
        self.chat_header = QLabel("Select a project to start chatting")
        chat_layout.addWidget(self.chat_header)
        
        # Messages display
        self.messages_display = QTextEdit()
        self.messages_display.setReadOnly(True)
        chat_layout.addWidget(self.messages_display)
        
        # Message input
        input_layout = QHBoxLayout()
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        self.message_input.setPlaceholderText("Type your message here...")
        input_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setEnabled(False)
        input_layout.addWidget(self.send_button)
        
        chat_layout.addLayout(input_layout)
        splitter.addWidget(chat_widget)
        
        layout.addWidget(splitter)
        
        # Set style
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #2196f3;
                color: white;
            }
        """)
        
    def load_projects(self):
        """Load available projects"""
        self.projects_list.clear()
        result = self.collaboration_system.get_user_projects(self.current_user)
        if result["status"] == "success":
            for project in result["projects"]:
                self.projects_list.addItem(project["name"])
                
    def project_selected(self, item):
        """Handle project selection"""
        project_name = item.text()
        result = self.collaboration_system.get_project_by_name(project_name)
        if result["status"] == "success":
            self.current_project = result["project"]
            self.chat_header.setText(f"Project: {project_name}")
            self.send_button.setEnabled(True)
            self.load_messages()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to load project."
            )
            
    def create_project(self):
        """Create a new project"""
        name = self.project_name_input.text().strip()
        description = self.project_desc_input.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter a project name."
            )
            return
            
        result = self.collaboration_system.create_project(
            name=name,
            description=description,
            owner=self.current_user
        )
        
        if result["status"] == "success":
            self.project_name_input.clear()
            self.project_desc_input.clear()
            self.load_projects()
        else:
            QMessageBox.warning(
                self,
                "Error",
                result.get("message", "Failed to create project.")
            )
            
    def send_message(self):
        """Send a message in the current project"""
        if not self.current_project:
            return
            
        message = self.message_input.toPlainText().strip()
        if not message:
            return
            
        result = self.collaboration_system.send_message(
            project_id=self.current_project["id"],
            sender=self.current_user,
            content=message
        )
        
        if result["status"] == "success":
            self.message_input.clear()
            self.load_messages()
            self.message_sent.emit(message)
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to send message."
            )
            
    def load_messages(self):
        """Load messages for the current project"""
        if not self.current_project:
            return
            
        result = self.collaboration_system.get_messages(
            project_id=self.current_project["id"]
        )
        
        if result["status"] == "success":
            self.messages_display.clear()
            for message in result["messages"]:
                timestamp = datetime.fromisoformat(message["timestamp"])
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                self.messages_display.append(
                    f'[{formatted_time}] {message["sender"]}: {message["content"]}'
                )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to load messages."
            )
            
    def closeEvent(self, event):
        """Handle dialog close event"""
        # Save any necessary state
        event.accept()
