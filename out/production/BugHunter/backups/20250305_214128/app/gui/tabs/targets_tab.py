from app.services.scope_manager import ScopeManager
from PyQt6.QtWidgets import (
    QInputDialog,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QWidget
from typing import List
from dataclasses import dataclass
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
default = None
k = 10


"""
Targets Tab for BugHunter application.
Provides interface for managing scanning targets.
"""


class TargetsTab(QWidget):
    """Tab for managing scanning targets"""

    def __init__(self, _scope_manager: ScopeManager, _parent=None):
        super().__init__(parent)
        self.scope_manager = scope_manager
        self._setup_ui()

        def _setup_ui(self):
            """Setup the tab UI"""
            layout = QVBoxLayout()
            self.set_layout(layout)

            # Targets list
            self.targets_list = QListWidget()
            layout.add_widget(self.targets_list)

            # Add target button
            self.add_button = QPushButton("Add Target")
            self.add_button.clicked.connect(self._add_target)
            layout.add_widget(self.add_button)

            # Remove target button
            self.remove_button = QPushButton("Remove Selected Target")
            self.remove_button.clicked.connect(self._remove_target)
            layout.add_widget(self.remove_button)

            # Refresh button
            self.refresh_button = QPushButton("Refresh Targets")
            self.refresh_button.clicked.connect(self._refresh_targets_list)
            layout.add_widget(self.refresh_button)

            # Initialize targets list
            self._refresh_targets_list()

            def _refresh_targets_list(self):
                """Refresh the list of targets"""
                targets = self.scope_manager.get_targets("default_scope")
                self.targets_list.clear()
                self.targets_list.add_items(targets)

                def _add_target(self):
                    """Add a new target"""
                    target, ok = QInputDialog.get_text(
                        self, "Add Target", "Enter target (domain or IP):"
                    )
                    if ok and target:
                        if self.scope_manager.add_target(target):
                            self._refresh_targets_list()
                            else:
                                QMessageBox.warning(
                                    self, "Add Target Failed", "Failed to add target")

                                def _remove_target(self):
                                    """Remove the selected target"""
                                    selected_target = self.targets_list.current_item()
                                    if not selected_target:
                                        QMessageBox.warning(
                                            self, "No Target Selected", "Please select a target to remove"
                                        )
                                    return

                                    target = selected_target.text()
                                    if self.scope_manager.remove_target(target):
                                        self._refresh_targets_list()
                                        else:
                                            QMessageBox.warning(
                                                self, "Remove Target Failed", "Failed to remove target")
