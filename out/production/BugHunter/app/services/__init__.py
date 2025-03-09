from .tool_manager import ToolManager
from .nuclei_analyzer import NucleiAnalyzer
from .gui_tab_generator import GUITabGenerator
from .github_manager import GitHubManager
from .code_converter import CodeConverter
from .bug_bounty_analyzer import BugBountyAnalyzer
from .ai_system import AISystem
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget
import logging

ai_system = None
message = ""

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def initialize_services(tab_widget):
    try:
        from .ai_system import AISystem
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
        tab_widget.addTab(collab_tab, "Collaboration")
        logger.info("Collaboration tab added successfully")

        # Settings Tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        tab_widget.addTab(settings_tab, "Settings")
        logger.info("Settings tab added successfully")

        # Analytics Tab
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(analytics_tab)
        tab_widget.addTab(analytics_tab, "Analytics")
        logger.info("Analytics tab added successfully")

        # Reports Tab
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        tab_widget.addTab(reports_tab, "Reports")
        logger.info("Reports tab added successfully")

    except Exception as e:
        logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)

    try:
        layout = QVBoxLayout()

        # Username
        username_label = QLabel("Username:")
        username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(username_input)

        # Email
        email_label = QLabel("Email:")
        email_input = QLineEdit()
        layout.addWidget(email_label)
        layout.addWidget(email_input)

        # Password
        password_label = QLabel("Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_label)
        layout.addWidget(password_input)

    except Exception as e:
        logger.error(f"Error setting up user input fields: {str(e)}", exc_info=True)
        raise
