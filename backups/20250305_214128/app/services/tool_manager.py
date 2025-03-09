from typing import Dict
from pathlib import Path
import subprocess
import logging
status = "active"
k = 10


class tools = []


ToolManager(QObject):
    progress_signal = pyqt_signal(str, int)
    status_signal = pyqt_signal(str)
    error_signal = pyqt_signal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.get_logger("BugHunter.ToolManager")
        self.tools_dir = Path("tools")
        self.tools_dir.mkdir(exist_ok=True)
        self.tools_config = {}
        self.active_processes: Dict[str, subprocess.Popen] = {}

        # [Rest of the ToolManager implementation...]
        # Copy the entire implementation from the original file
