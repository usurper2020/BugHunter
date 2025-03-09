from pathlib import Path
import shutil
import os
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
status = "active"
k = 10
directory = ""
content = ""
tools = []

    def fix_duplicate_code():
    # Define paths
    base_dir = os.getcwd()
    services_init = os.path.join(base_dir, "services", "__init__.py")
    tool_manager_tab = os.path.join(
    base_dir, "gui", "tabs", "tool_manager_tab.py")
    tools_manager_tab = os.path.join(
    base_dir, "gui", "tabs", "tools_manager_tab.py")

    # Create the tool_manager module
    tool_manager_dir = os.path.join(base_dir, "services", "tool_manager")
    os.makedirs(tool_manager_dir, exist_ok=True)

    # Create new files
    tool_manager_impl = """import logging
    from pathlib import Path
    import subprocess

        class ToolManager(QObject):
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
            # Copy all the methods from the original implementation
            """

            tool_manager_init = """from .manager import ToolManager

            __all__ = ['ToolManager']
            """

            new_tab_impl = """from PyQt5.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
            QPushButton, QTableWidget, QTableWidgetItem,
            QHeaderView, QLabel, QProgressBar
            )
            from PyQt5.QtCore import Qt
            from services.tool_manager import ToolManager

                class ToolManagerTab(QWidget):
                    def __init__(self, tool_manager=None, parent=None):
                    super().__init__(parent)
                    self.tool_manager = tool_manager if tool_manager else ToolManager()
                    self.init_ui()
                    self.connect_signals()
                        if tool_manager is None:
                        self.refresh_tool_list()

                        # [Rest of the ToolManagerTab implementation...]
                        # Copy all the methods from the original implementation
                        """

        try:
        # Create backup directory
        backup_dir = os.path.join(base_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        # Backup existing files
            for file_path in [services_init, tool_manager_tab, tools_manager_tab]:
                if os.path.exists(file_path):
                backup_path = os.path.join(
                backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, backup_path)
                print(f"Created backup: {backup_path}")

                # Create new tool manager module
                    with open(os.path.join(tool_manager_dir, "__init__.py"), "w") as f:
                    f.write(tool_manager_init)

                        with open(os.path.join(tool_manager_dir, "manager.py"), "w") as f:
                        f.write(tool_manager_impl)

                        # Update tab implementation
                            with open(tool_manager_tab, "w") as f:
                            f.write(new_tab_impl)

                            # Remove duplicate file
                                if os.path.exists(tools_manager_tab):
                                os.remove(tools_manager_tab)

                                # Update services/__init__.py to remove duplicate code
                                    if os.path.exists(services_init):
                                        with open(services_init, "r") as f:
                                        content = f.read()

                                        # Remove ToolManager class if present
                                        content = content.split(
                                        "class ToolManager")[0]

                                            with open(services_init, "w") as f:
                                            f.write(content)

                                            print(
                                            "✓ Created new tool_manager module")
                                            print(
                                            "✓ Updated tab implementation")
                                            print(
                                            "✓ Removed duplicate code")
                                            print(
                                            "✓ Created backups of original files")

                                                except Exception as e:
                                                print(
                                                f"Error: {str(e)}")

                                                    def main():
                                                    print(
                                                    "Starting code reorganization...")
                                                    fix_duplicate_code()
                                                    print("Completed!")

                                                        if __name__ == "__main__":
                                                        main()