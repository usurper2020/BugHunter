"""Scope tab implementation for the BugHunter application."""

from PyQt6.QtWidgets import (
    QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QGroupBox, QListWidget
)
from PyQt6.QtCore import Qt, pyqtSlot
from services.scope_manager import ScopeManager
from .base_tab import BaseTab
import logging

class ScopeTab(BaseTab):
    """Scope management interface tab"""
    
    def __init__(self, scope_manager: ScopeManager, parent=None):
        self.scope_manager = scope_manager
        self.logger = logging.getLogger('BugHunter.ScopeTab')
        self.logger.debug("Initializing ScopeTab")
        super().__init__(parent)


 
    def _setup_ui(self):
        """Setup the UI components"""
        # Create scope list section
        scope_group = QGroupBox("Current Scope")
        scope_layout = QVBoxLayout()
        scope_group.setLayout(scope_layout)
        
        self.scope_list = QListWidget()
        self._refresh_scope_list()
        scope_layout.addWidget(self.scope_list)
        
        # Create scope management section
        management_group = QGroupBox("Scope Management")
        management_layout = QVBoxLayout()
        management_group.setLayout(management_layout)
        
        input_layout = QHBoxLayout()
        self.scope_input = QLineEdit()
        self.scope_input.setPlaceholderText("Enter new scope item...")
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self._add_scope_item)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self._remove_scope_item)
        
        input_layout.addWidget(self.scope_input)
        input_layout.addWidget(self.add_button)
        management_layout.addLayout(input_layout)
        management_layout.addWidget(self.remove_button)
        
        # Add status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        
        # Add all components to main layout
        self.layout.addWidget(scope_group)
        self.layout.addWidget(management_group)
        self.layout.addWidget(status_group)
        
        self._update_status("Scope manager ready.")
    
    def _refresh_scope_list(self):
        """Refresh the list of scope items"""
        self.logger.debug("Refreshing scope list")
        self.scope_list.clear()
        try:
            targets = self.scope_manager.get_targets('default_scope')
            self.logger.debug(f"Retrieved {len(targets)} targets from scope manager")
            if not targets:
                self._update_status("No targets found in default scope")
                self.logger.debug("No targets found in default scope")
            for target in targets:
                self.scope_list.addItem(target)
                self.logger.debug(f"Added target to list: {target}")
        except Exception as e:
            error_msg = f"Error loading scope: {str(e)}"
            self._update_status(error_msg)
            self.logger.error(error_msg, exc_info=True)




    
    def _update_status(self, message: str):
        """Update status message"""
        self.status_label.setText(message)
        self.logger.info(message)
    
    @pyqtSlot()
    def _add_scope_item(self):
        """Handle adding a new scope item"""
        new_item = self.scope_input.text().strip()
        self.logger.debug(f"Attempting to add scope item: {new_item}")
        if not new_item:
            msg = "Please enter a scope item"
            self._update_status(msg)
            self.logger.debug(msg)
            return
        
        try:
            # Validate the target format
            if not self._validate_target(new_item):
                msg = "Invalid target format"
                self._update_status(msg)
                self.logger.debug(msg)
                return
                
            # Add target and refresh
            if self.scope_manager.add_target(new_item):
                self.logger.debug(f"Successfully added target: {new_item}")
                self._refresh_scope_list()
                self.scope_input.clear()
                msg = f"Added '{new_item}' to scope"
                self._update_status(msg)
                self.logger.info(msg)
            else:
                msg = f"Failed to add '{new_item}'"
                self._update_status(msg)
                self.logger.warning(msg)
        except Exception as e:
            error_msg = f"Error adding scope item: {str(e)}"
            self._update_status(error_msg)
            self.logger.error(error_msg, exc_info=True)


    
    @pyqtSlot()
    def _remove_scope_item(self):
        """Handle removing selected scope item"""
        selected_items = self.scope_list.selectedItems()
        if not selected_items:
            self._update_status("Please select an item to remove")
            return
        
        try:
            for item in selected_items:
                self.scope_manager.remove_target(item.text())

            self._refresh_scope_list()
            self._update_status("Removed selected items from scope")
        except Exception as e:
            self._update_status(f"Error removing scope item: {str(e)}")
            self.logger.error(f"Error removing scope item: {str(e)}")
    
    def _validate_target(self, target: str) -> bool:
        """Validate target format"""
        # Basic validation - could be expanded with regex
        return bool(target and len(target) > 3 and '.' in target)

    def refresh(self):
        """Refresh tab content"""
        try:
            self._refresh_scope_list()
            self._update_status("Scope manager refreshed.")
        except Exception as e:
            self._update_status(f"Error refreshing scope: {str(e)}")
            self.logger.error(f"Error refreshing scope: {str(e)}")
