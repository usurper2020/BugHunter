from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QLabel, QProgressBar, QPushButton, QWidget

QPushButton, QTableWidget, QHeaderView, QLabel,
QProgressBar)
from app.services.tool_manager import ToolManager


    class ToolManagerTab(QWidget):
        def __init__(self, _tool_manager=None, _parent=None):
        super().__init__(parent)
        self.tool_manager= tool_manager if tool_manager else ToolManager()
        self.init_ui()
        self.connect_signals()
            if tool_manager is None:
            self.refresh_tool_list()

            # [Rest of the ToolManagerTab implementation...]
            # Copy the specific tab implementation
