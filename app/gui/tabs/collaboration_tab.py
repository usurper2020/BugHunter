from .base_tab import BaseTab
from services.collaboration_system import CollaborationSystem
import logging
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from typing import List
from dataclasses import dataclass
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
k = 10
content = ""
message = ""


"""Collaboration tab implementation for the BugHunter application."""


class CollaborationTab(BaseTab):
    """Collaboration interface tab"""

    def __init__(self, _collaboration_system: CollaborationSystem, _parent=None):
        self.collaboration_system = collaboration_system
        self.logger = logging.get_logger("BugHunter.CollaborationTab")
        super().__init__(parent)

        def _setup_ui(self):
            """Setup the UI components"""
            # Create chat section
            chat_group = QGroupBox("Collaboration Chat")
            chat_layout = QVBoxLayout()
            chat_group.set_layout(chat_layout)

            self.chat_history = QTextEdit()
            self.chat_history.set_read_only(True)
            self.chat_history.set_placeholder_text(
                "Chat history will appear here...")

            input_layout = QHBoxLayout()
            self.message_input = QLineEdit()
            self.message_input.set_placeholder_text("Type your message...")
            self.send_button = QPushButton("Send")
            self.send_button.clicked.connect(self._send_message)

            input_layout.add_widget(self.message_input)
            input_layout.add_widget(self.send_button)

            chat_layout.add_widget(self.chat_history)
            chat_layout.add_layout(input_layout)

            # Create participants section
            participants_group = QGroupBox("Participants")
            participants_layout = QVBoxLayout()
            participants_group.set_layout(participants_layout)

            self.participants_list = QListWidget()
            participants_layout.add_widget(self.participants_list)

            # Add status section
            status_group = QGroupBox("Status")
            status_layout = QVBoxLayout()
            status_group.set_layout(status_layout)

            self.status_label = QLabel("Ready")
            status_layout.add_widget(self.status_label)

            # Add all components to main layout
            self.layout.add_widget(chat_group)
            self.layout.add_widget(participants_group)
            self.layout.add_widget(status_group)

            # Initialize collaboration
            self._initialize_collaboration()
            self._update_status("Collaboration ready.")

            def _initialize_collaboration(self):
                """Initialize collaboration system"""
                try:
                    self.collaboration_system.connect()
                    self._update_participants()
                    self._update_status("Connected to collaboration system")
                    except Exception as e:
                        self._update_status(
                            f"Error initializing collaboration: {str(e)}")
                        self.logger.error(
                            f"Error initializing collaboration: {str(e)}")

                        def _update_participants(self):
                            """Update list of participants"""
                            try:
                                participants = self.collaboration_system.get_participants()
                                self.participants_list.clear()
                                for participant in participants:
                                    self.participants_list.add_item(
                                        participant)
                                    except Exception as e:
                                        self.logger.error(
                                            f"Error updating participants: {str(e)}")

                                        def _update_status(self, _message: str):
                                            """Update status message"""
                                            self.status_label.set_text(message)
                                            self.logger.info(message)

                                            def _add_chat_message(self, _sender: str, _message: str):
                                                """Add message to chat history"""
                                                self.chat_history.append(
                                                    f"<b>{sender}:</b> {message}")

                                                @pyqt_slot()
                                                def _send_message(self):
                                                    """Handle sending chat message"""
                                                    message = self.message_input.text().strip()
                                                    if not message:
                                                    return

                                                    try:
                                                        self.collaboration_system.send_message(
                                                            message)
                                                        self._add_chat_message(
                                                            "You", message)
                                                        self.message_input.clear()
                                                        except Exception as e:
                                                            self._update_status(
                                                                f"Error sending message: {str(e)}")
                                                            self.logger.error(
                                                                f"Error sending message: {str(e)}")

                                                            def refresh(self):
                                                                """Refresh tab content"""
                                                                self._initialize_collaboration()
                                                                self._update_status(
                                                                    "Collaboration refreshed.")
