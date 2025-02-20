"""
Scope Tab Module.

This module provides the scope management interface for BugHunter,
allowing users to define and manage their scanning scope.

Classes:
    ScopeTab: Scope management tab class.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal

class ScopeTab(QWidget):
    """
    Scope management tab for BugHunter.

    Attributes:
        scope_list (QListWidget): List widget for displaying scope items.
        scope_input (QLineEdit): Input field for new scope items.
        add_button (QPushButton): Button to add new scope items.
        remove_button (QPushButton): Button to remove selected scope items.
    """

    scope_updated = pyqtSignal(list)
    status_message = pyqtSignal(str)

    def __init__(self):
        """Initialize the scope management tab."""
        super().__init__()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout()

        # Scope list
        self.scope_list = QListWidget()
        layout.addWidget(QLabel("Current Scope:"))
        layout.addWidget(self.scope_list)

        # Scope input section
        input_layout = QHBoxLayout()
        self.scope_input = QLineEdit()
        self.scope_input.setPlaceholderText("Enter new scope item (e.g., example.com)")
        input_layout.addWidget(self.scope_input)

        self.add_button = QPushButton("Add")
        input_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        input_layout.addWidget(self.remove_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def connect_signals(self):
        """Connect UI signals to appropriate slots."""
        self.add_button.clicked.connect(self.add_scope_item)
        self.remove_button.clicked.connect(self.remove_scope_item)

    def add_scope_item(self):
        """Add a new item to the scope list."""
        new_item = self.scope_input.text().strip()
        if new_item:
            self.scope_list.addItem(new_item)
            self.scope_input.clear()
            self.update_scope()
            self.status_message.emit(f"Added scope item: {new_item}")
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid scope item")

    def remove_scope_item(self):
        """Remove selected items from the scope list."""
        selected_items = self.scope_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.scope_list.takeItem(self.scope_list.row(item))
                self.status_message.emit(f"Removed scope item: {item.text()}")
            self.update_scope()
        else:
            QMessageBox.warning(self, "No Selection", "Please select items to remove")

    def get_scope(self):
        """Get the current scope as a list of strings.
        
        Returns:
            list: List of scope items.
        """
        return [self.scope_list.item(i).text() for i in range(self.scope_list.count())]

    def update_scope(self):
        """Emit the updated scope list."""
        current_scope = self.get_scope()
        self.scope_updated.emit(current_scope)

    def cleanup(self):
        """Clean up resources before closing."""
        self.scope_list.clear()

    def load_scope(self, scope_items):
        """Load scope items into the list.
        
        Args:
            scope_items (list): List of scope items to load.
        """
        self.scope_list.clear()
        for item in scope_items:
            self.scope_list.addItem(item)
        self.update_scope()
