from PyQt6.QtWidgets import QLabel, QProgressBar, QPushButton, QWidget
from typing import Dict
from pathlib import Path
from dataclasses import dataclass
import shutil
import logging
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget
status = "active"
k = 10
directory = ""
tools = []


@dataclass
    class CodeDuplicateResolver:
        def __init__(self):
        self.logger = logging.get_logger("BugHunter.DuplicateResolver")
        self.base_dir = Path("app")

            def resolve_tool_manager_duplication(self):
            """
                Resolves the duplicate ToolManager implementation by:
                1. Creating a common service module
                2. Moving the shared code there
                3. Updating the importing files
                """
                   try:
                   # 1. Create services directory if it doesn't exist
                   services_dir = self.base_dir / "services"
                   services_dir.mkdir(exist_ok=True)

                   # 2. Create tool_manager.py in services
                   self._create_tool_manager_service()

                   # 3. Update the importing files
                   self._update_importing_files()

                   self.logger.info(
                   "Successfully resolved ToolManager duplication")
                return True

                    except Exception as e:
                    self.logger.error(
                    f"Failed to resolve duplication: {str(e)}")
                return False

                    def _create_tool_manager_service(self):
                    """Creates the centralized ToolManager service"""
                    service_content = """
                    from pathlib import Path
                    import logging
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
                            # Copy the entire implementation from the original file
                            """

                            # Write the service file
                            service_file = self.base_dir / "services" / "tool_manager.py"
                            with open(service_file, "w", encoding="utf-8") as f:
                            f.write(service_content)

                                def _update_importing_files(self):
                                """Updates the files that were using the duplicate code"""
                                files_to_update = [
                                self.base_dir / "gui" / "tabs" / "tool_manager_tab.py",
                                self.base_dir / "gui" / "tabs" / "tools_manager_tab.py",
                                ]

                                new_content = """
                                QPushButton, QTableWidget, QHeaderView, QLabel,
                                QProgressBar)
                                from app.services.tool_manager import ToolManager

                                        class ToolManagerTab(QWidget):
                                            def __init__(self, _tool_manager=None, _parent=None):
                                            super().__init__(parent)
                                            self.tool_manager = tool_manager if tool_manager else ToolManager()
                                            self.init_ui()
                                            self.connect_signals()
                                                if tool_manager is None:
                                                self.refresh_tool_list()

                                                # [Rest of the ToolManagerTab implementation...]
                                                # Copy the specific tab implementation
                                                """

                                       for file_path in files_to_update:
                                            if file_path.exists():
                                            # Backup the original file
                                            backup_path = file_path.with_suffix(
                                            ".py.bak")
                                            shutil.copy2(
                                            file_path, backup_path)

                                            # Write the new content
                                                with open(file_path, "w", encoding="utf-8") as f:
                                                f.write(new_content)

                                                    def main():
                                                    """Main function to resolve code duplication"""
                                                    logging.basic_config(
                                                    level=logging.INFO)

                                                    resolver = CodeDuplicateResolver()
                                                        if resolver.resolve_tool_manager_duplication():
                                                        print(
                                                        "Successfully resolved code duplication")
                                                            else:
                                                            print(
                                                            "Failed to resolve code duplication")

                                                                if __name__ == "__main__":
                                                                main()