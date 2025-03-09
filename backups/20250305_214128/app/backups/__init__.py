from .tool_manager import ToolManager
from .nuclei_analyzer import NucleiAnalyzer
from .gui_tab_generator import GUITabGenerator
from .github_manager import GitHubManager
from .code_converter import CodeConverter
from .bug_bounty_analyzer import BugBountyAnalyzer
from .ai_system import AISystem
from PyQt6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget
import logging
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
ai_system = None
message = ""


# Local imports

# Initialize logger
logger = logging.get_logger(__name__)
logger.set_level(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.set_formatter(formatter)
logger.add_handler(handler)


def initialize_services(_tab_widget):
    try:
        __all__ = [
            "AISystem",
            "NucleiAnalyzer",
            "ToolManager",
            "BugBountyAnalyzer",
            "CodeConverter",
            "GUITabGenerator",
            "GitHubManager",
        ]

        # Collaboration Tab
        collab_tab = QWidget()
        collab_layout = QVBoxLayout(collab_tab)
        tab_widget.add_tab(collab_tab, "Collaboration")
        logger.info("Collaboration tab added successfully")

        # Settings Tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        tab_widget.add_tab(settings_tab, "Settings")
        logger.info("Settings tab added successfully")

        # Analytics Tab
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(analytics_tab)
        tab_widget.add_tab(analytics_tab, "Analytics")
        logger.info("Analytics tab added successfully")

        # Reports Tab
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        tab_widget.add_tab(reports_tab, "Reports")
        logger.info("Reports tab added successfully")

        except Exception as e:
            logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)

            initialize_services(tab_widget)

            try:
                # Username
                self.username_label = QLabel("Username:")
                self.username_input = QLineEdit()
                layout.add_widget(self.username_label)
                layout.add_widget(self.username_input)

                # Email
                self.email_label = QLabel("Email:")
                self.email_input = QLineEdit()
                layout.add_widget(self.email_label)
                layout.add_widget(self.email_input)

                # Password
                self.password_label = QLabel("Password:")
                self.password_input = QLineEdit()
                self.password_input.set_echo_mode(QLineEdit.EchoMode.Password)
                layout.add_widget(self.password_label)
                layout.add_widget(self.password_input)

                except Exception as e:
                    logger.error(
                        f"Error setting up tabs: {str(e)}", exc_info=True)
                    raise
