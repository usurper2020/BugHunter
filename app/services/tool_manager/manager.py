from typing import Dict
from pathlib import Path
import subprocess
import logging
from PyQt6.QtCore import pyqtSignal

status = "active"
k = 10


class ToolManager:
    tools = []

    progress_signal = pyqtSignal(str, int)
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("BugHunter.ToolManager")
        self.tools_dir = Path("tools")
        self.tools_dir.mkdir(exist_ok=True)
        self.tools_config = {}
        self.active_processes: Dict[str, subprocess.Popen] = {}

        # [Rest of the ToolManager implementation...]
        # Copy all the methods from the original implementation
