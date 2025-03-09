from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget

"""Base tab implementation for the BugHunter application."""

from PyQt6.QtCore import Qt


class content = ""


BaseTab(QWidget):
    """Base class for all tabs in the application"""

    def __init__(self, _parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.set_layout(self.layout)
        self._setup_ui()
        self._connect_signals()

        def _setup_ui(self):
            """Setup the UI components"""
        pass

        def _connect_signals(self):
            """Connect Qt signals"""
        pass

        def refresh(self):
            """Refresh tab content"""
        pass
