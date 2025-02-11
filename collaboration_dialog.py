from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QLabel, QLineEdit, QTextEdit, QPushButton, 
                            QComboBox, QTableWidget, QTableWidgetItem,
                            QMessageBox, QWidget)
from PyQt6.QtCore import Qt
import json

class CollaborationDialog(QDialog):
    def __init__(self, collaboration_system, current_user, parent=None):
        super().__init__(parent)
        self.collaboration_system = collaboration_system
        self.current_user = current_user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Collaboration Center')
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create individual tabs
        self.messages_tab = QWidget()
        self.tasks_tab = QWidget()
        self.notes_tab = QWidget()
        
        # Add tabs to widget
        self.tabs.addTab(self.messages_tab, "Messages")
        self.tabs.addTab(self.tasks_tab, "Tasks")
        self.tabs.addTab(self.notes_tab, "Notes")
        
        # Set up each tab
        self.setup_messages_tab()
        self.setup_tasks_tab()
        self.setup_notes_tab()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def setup_messages_tab(self):
        layout = QVBoxLayout(self.messages_tab)
        
        # Message composition section
        compose_layout = QHBoxLayout()
        
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("Recipient username")
        compose_layout.addWidget(self.recipient_input)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type your message here")
        self.message_input.setMaximumHeight(100)
        compose_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        compose_layout.addWidget(self.send_button)
        
        layout.addLayout(compose_layout)
        
        # Messages display section
        self.messages_display = QTextEdit()
        self.messages_display.setReadOnly(True)
        layout.addWidget(self.messages_display)
        
        # Refresh button
        self.refresh_messages_button = QPushButton("Refresh Messages")
        self.refresh_messages_button.clicked.connect(self.refresh_messages)
        layout.addWidget(self.refresh_messages_button)
        
        # Initial load of messages
        self.refresh_messages()

    def setup_tasks_tab(self):
        layout = QVBoxLayout(self.tasks_tab)
        
        # Task creation section
        create_layout = QHBoxLayout()
        
        self.task_title_input = QLineEdit()
        self.task_title_input.setPlaceholderText("Task title")
        create_layout.addWidget(self.task_title_input)
        
        self.task_assignee_input = QLineEdit()
        self.task_assignee_input.setPlaceholderText("Assignee username")
        create_layout.addWidget(self.task_assignee_input)
        
        self.task_priority_combo = QComboBox()
        self.task_priority_combo.addItems(['low', 'medium', 'high'])
        create_layout.addWidget(self.task_priority_combo)
        
        layout.addLayout(create_layout)
        
        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Task description")
        self.task_description_input.setMaximumHeight(100)
        layout.addWidget(self.task_description_input)
        
        self.create_task_button = QPushButton("Create Task")
        self.create_task_button.clicked.connect(self.create_task)
        layout.addWidget(self.create_task_button)
        
        # Tasks display section
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(6)
        self.tasks_table.setHorizontalHeaderLabels(['Title', 'Assignee', 'Priority', 'Status', 'Created', 'Actions'])
        layout.addWidget(self.tasks_table)
        
        # Refresh button
        self.refresh_tasks_button = QPushButton("Refresh Tasks")
        self.refresh_tasks_button.clicked.connect(self.refresh_tasks)
        layout.addWidget(self.refresh_tasks_button)
        
        # Initial load of tasks
        self.refresh_tasks()

    def setup_notes_tab(self):
        layout = QVBoxLayout(self.notes_tab)
        
        # Note creation section
        create_layout = QHBoxLayout()
        
        self.note_title_input = QLineEdit()
        self.note_title_input.setPlaceholderText("Note title")
        create_layout.addWidget(self.note_title_input)
        
        self.note_tags_input = QLineEdit()
        self.note_tags_input.setPlaceholderText("Tags (comma-separated)")
        create_layout.addWidget(self.note_tags_input)
        
        layout.addLayout(create_layout)
        
        self.note_content_input = QTextEdit()
        self.note_content_input.setPlaceholderText("Note content")
        layout.addWidget(self.note_content_input)
        
        self.create_note_button = QPushButton("Create Note")
        self.create_note_button.clicked.connect(self.create_note)
        layout.addWidget(self.create_note_button)
        
        # Notes display section
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(5)
        self.notes_table.setHorizontalHeaderLabels(['Title', 'Tags', 'Created', 'Updated', 'Actions'])
        layout.addWidget(self.notes_table)
        
        # Search section
        search_layout = QHBoxLayout()
        
        self.note_search_input = QLineEdit()
        self.note_search_input.setPlaceholderText("Search notes...")
        search_layout.addWidget(self.note_search_input)
        
        self.search_notes_button = QPushButton("Search")
        self.search_notes_button.clicked.connect(self.search_notes)
        search_layout.addWidget(self.search_notes_button)
        
        layout.addLayout(search_layout)
        
        # Refresh button
        self.refresh_notes_button = QPushButton("Refresh Notes")
        self.refresh_notes_button.clicked.connect(self.refresh_notes)
        layout.addWidget(self.refresh_notes_button)
        
        # Initial load of notes
        self.refresh_notes()

    def send_message(self):
        recipient = self.recipient_input.text()
        content = self.message_input.toPlainText()
        
        if not recipient or not content:
            QMessageBox.warning(self, 'Error', 'Please enter both recipient and message')
            return
        
        result = self.collaboration_system.send_message(self.current_user, recipient, content)
        if result['status'] == 'success':
            self.message_input.clear()
            self.refresh_messages()
            QMessageBox.information(self, 'Success', 'Message sent successfully')
        else:
            QMessageBox.warning(self, 'Error', result['message'])

    def refresh_messages(self):
        messages = self.collaboration_system.get_messages(self.current_user)
        display_text = ""
        
        for message in sorted(messages, key=lambda x: x['timestamp']):
            if message['sender'] == self.current_user:
                display_text += f"You -> {message['recipient']}: {message['content']}\n"
            else:
                display_text += f"{message['sender']} -> You: {message['content']}\n"
            display_text += f"[{message['timestamp']}]\n\n"
        
        self.messages_display.setText(display_text)

    def create_task(self):
        title = self.task_title_input.text()
        assignee = self.task_assignee_input.text()
        description = self.task_description_input.toPlainText()
        priority = self.task_priority_combo.currentText()
        
        if not title or not assignee or not description:
            QMessageBox.warning(self, 'Error', 'Please fill in all task fields')
            return
        
        result = self.collaboration_system.create_task(
            self.current_user, assignee, title, description, priority)
        
        if result['status'] == 'success':
            self.task_title_input.clear()
            self.task_assignee_input.clear()
            self.task_description_input.clear()
            self.refresh_tasks()
            QMessageBox.information(self, 'Success', 'Task created successfully')
        else:
            QMessageBox.warning(self, 'Error', result['message'])

    def refresh_tasks(self):
        tasks = self.collaboration_system.get_tasks(self.current_user)
        self.tasks_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            self.tasks_table.setItem(row, 0, QTableWidgetItem(task['title']))
            self.tasks_table.setItem(row, 1, QTableWidgetItem(task['assignee']))
            self.tasks_table.setItem(row, 2, QTableWidgetItem(task['priority']))
            self.tasks_table.setItem(row, 3, QTableWidgetItem(task['status']))
            self.tasks_table.setItem(row, 4, QTableWidgetItem(task['created_at']))
            
            # Add status update button
            if task['assignee'] == self.current_user:
                update_button = QPushButton('Update Status')
                update_button.clicked.connect(lambda checked, t=task: self.update_task_status(t))
                self.tasks_table.setCellWidget(row, 5, update_button)
        
        self.tasks_table.resizeColumnsToContents()

    def update_task_status(self, task):
        status_combo = QComboBox()
        status_combo.addItems(['pending', 'in_progress', 'completed'])
        status_combo.setCurrentText(task['status'])
        
        dialog = QDialog(self)
        dialog.setWindowTitle('Update Task Status')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('New Status:'))
        layout.addWidget(status_combo)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec():
            result = self.collaboration_system.update_task_status(task['id'], status_combo.currentText())
            if result['status'] == 'success':
                self.refresh_tasks()
                QMessageBox.information(self, 'Success', 'Task status updated successfully')
            else:
                QMessageBox.warning(self, 'Error', result['message'])

    def create_note(self):
        title = self.note_title_input.text()
        content = self.note_content_input.toPlainText()
        tags = [tag.strip() for tag in self.note_tags_input.text().split(',') if tag.strip()]
        
        if not title or not content:
            QMessageBox.warning(self, 'Error', 'Please enter both title and content')
            return
        
        result = self.collaboration_system.add_note(self.current_user, title, content, tags)
        if result['status'] == 'success':
            self.note_title_input.clear()
            self.note_content_input.clear()
            self.note_tags_input.clear()
            self.refresh_notes()
            QMessageBox.information(self, 'Success', 'Note created successfully')
        else:
            QMessageBox.warning(self, 'Error', result['message'])

    def refresh_notes(self):
        notes = self.collaboration_system.get_notes(self.current_user)
        self.notes_table.setRowCount(len(notes))
        
        for row, note in enumerate(notes):
            self.notes_table.setItem(row, 0, QTableWidgetItem(note['title']))
            self.notes_table.setItem(row, 1, QTableWidgetItem(', '.join(note['tags'])))
            self.notes_table.setItem(row, 2, QTableWidgetItem(note['created_at']))
            self.notes_table.setItem(row, 3, QTableWidgetItem(note['updated_at']))
            
            # Add share button
            share_button = QPushButton('Share')
            share_button.clicked.connect(lambda checked, n=note: self.share_note(n))
            self.notes_table.setCellWidget(row, 4, share_button)
        
        self.notes_table.resizeColumnsToContents()

    def search_notes(self):
        query = self.note_search_input.text()
        if not query:
            self.refresh_notes()
            return
        
        notes = self.collaboration_system.search_notes(query)
        self.notes_table.setRowCount(len(notes))
        
        for row, note in enumerate(notes):
            self.notes_table.setItem(row, 0, QTableWidgetItem(note['title']))
            self.notes_table.setItem(row, 1, QTableWidgetItem(', '.join(note['tags'])))
            self.notes_table.setItem(row, 2, QTableWidgetItem(note['created_at']))
            self.notes_table.setItem(row, 3, QTableWidgetItem(note['updated_at']))
            
            # Add share button
            share_button = QPushButton('Share')
            share_button.clicked.connect(lambda checked, n=note: self.share_note(n))
            self.notes_table.setCellWidget(row, 4, share_button)
        
        self.notes_table.resizeColumnsToContents()

    def share_note(self, note):
        share_with = QLineEdit()
        
        dialog = QDialog(self)
        dialog.setWindowTitle('Share Note')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Share with (username):'))
        layout.addWidget(share_with)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton('Share')
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec():
            username = share_with.text()
            if username:
                result = self.collaboration_system.share_note(note['id'], username)
                if result['status'] == 'success':
                    QMessageBox.information(self, 'Success', 'Note shared successfully')
                else:
                    QMessageBox.warning(self, 'Error', result['message'])
