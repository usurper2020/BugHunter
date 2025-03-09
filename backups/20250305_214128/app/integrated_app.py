from tabs.tool_tab import ToolTab
from tabs.ai_chat_tab import AIChatTab
from services.wayback_machine_integration import WaybackMachineIntegration
from services.vulnerability_scanner import VulnerabilityScanner
from services.vulnerability_database import VulnerabilityDatabase
from services.user_auth import UserAuth
from services.shodan_integration import ShodanIntegration
from services.scope_manager import ScopeManager
from services.scanning_profiles import ScanningProfiles
from services.role_manager import RoleManager
from services.report_generator import ReportGenerator
from services.login_dialog import LoginDialog
from services.contribution_system import ContributionSystem
from services.collaboration_system import CollaborationSystem
from services.collaboration import Collaboration
from services.analytics_system import AnalyticsSystem
from services.ai_training import AITraining
from services.ai_integration import AIIntegration
from tool_manager import ToolManager
from scanner_tab import ScannerTab
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from dataclasses import dataclass
import sys
import os
import json
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QTabWidget
status = "active"
key = ""
k = 10
directory = ""
tools = []


# Add project root to Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


logger = logger_config.get_logger(__name__)


class IntegratedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_window_title("Bug Hunter - Security Testing Tool")
        self.set_minimum_size(1200, 800)

        # Initialize UI first
        self.init_base_ui()

        # Initialize authentication and role management
        self.auth_manager = UserAuth()
        self.role_manager = RoleManager()
        self.user_token = None
        self.current_user = None
        self.user_role = None

        # Show login dialog
        if not self.show_login():
            sys.exit()

            # Initialize components
            self.init_components()
            self.create_tools_directory()
            self.init_ui()
            self.load_preferences()

            def init_components(self):
                """Initialize all system components"""
                try:
                    self.tool_manager = ToolManager()  # Initialize without parameters
                    self.ai_integration = AIIntegration()
                    self.ai_training = AITraining()
                    self.scope_manager = ScopeManager()
                    self.shodan_integration = ShodanIntegration(
                        config.get("SHODAN_API_KEY", "")
                    )
                    self.wayback_integration = WaybackMachineIntegration()
                    self.report_generator = ReportGenerator()
                    self.scanner = VulnerabilityScanner()
                    self.profiles_manager = ScanningProfiles()
                    self.vulnerability_database = VulnerabilityDatabase()
                    self.collaboration_system = CollaborationSystem()
                    self.analytics_system = AnalyticsSystem()
                    self.contribution_system = ContributionSystem()
                    except Exception as e:
                        logger.error(f"Error initializing components: {e}")
                        raise

                        def init_base_ui(self):
                            """Initialize base UI elements needed before login"""
                            central_widget = QWidget()
                            self.set_central_widget(central_widget)
                            main_layout = QVBoxLayout(central_widget)

                            # Add header
                            header = QLabel("Bug Hunter")
                            header.set_font(
                                QFont("Arial", 16, QFont.Weight.Bold))
                            header.set_alignment(Qt.AlignmentFlag.AlignCenter)
                            header.set_style_sheet(
                                "color: #2196f3; margin: 10px;")
                            main_layout.add_widget(header)

                            # Create log display
                            self.log_display = QTextEdit()
                            self.log_display.set_read_only(True)
                            self.log_display.append(
                                "Please log in to continue...")
                            main_layout.add_widget(self.log_display)

                            def init_ui(self):
                                """Initialize the main UI after successful login"""
                                # Create main layout
                                main_widget = QWidget()
                                main_layout = QVBoxLayout(main_widget)
                                self.set_central_widget(main_widget)

                                # Create tab widget
                                self.tabs = QTabWidget()
                                main_layout.add_widget(self.tabs)

                                # Add the log display to the new layout
                                old_widget = self.log_display.parent()
                                if old_widget:
                                    old_widget.layout().remove_widget(self.log_display)
                                    self.log_display.set_maximum_height(150)
                                    main_layout.add_widget(self.log_display)

                                    # Create and add tabs
                                    self.setup_tabs()

                                    # Set window style
                                    self.set_style_sheet(
                                        """
                                    QMainWindow {
                                    background-color: #f0f0f0;
                                    }
                                    QTabWidget::pane {
                                    border: 1px solid #cccccc;
                                    background: white;
                                    border-radius: 4px;
                                    }
                                    QTabBar::tab {
                                    background: #e0e0e0;
                                    padding: 8px 20px;
                                    margin: 2px;
                                    border-top-left-radius: 4px;
                                    border-top-right-radius: 4px;
                                    }
                                    QTabBar::tab:selected {
                                    background: #2196f3;
                                    color: white;
                                    }
                                    QTabBar::tab:hover:!selected {
                                    background: #90caf9;
                                    }
                                    QPushButton {
                                    background-color: #2196f3;
                                    color: white;
                                    border: none;
                                    padding: 8px 16px;
                                    border-radius: 4px;
                                    }
                                    QPushButton:hover {
                                    background-color: #1976d2;
                                    }
                                    QPushButton:pressed {
                                    background-color: #0d47a1;
                                    }
                                    QTextEdit {
                                    border: 1px solid #cccccc;
                                    border-radius: 4px;
                                    padding: 4px;
                                    }
                                    QLabel {
                                    color: #333333;
                                    }
                                    """
                                    )

                                    def setup_tabs(self):
                                        """Set up all application tabs"""
                                        try:
                                            # AI Assistant Tab
                                            self.ai_chat_tab = AIChatTab(self)
                                            self.tabs.add_tab(
                                                self.ai_chat_tab, "AI Assistant")
                                            logger.info(
                                                "AI Assistant tab added successfully")

                                            # Scanner Tab
                                            self.scanner_tab = ScannerTab(self)
                                            self.tabs.add_tab(
                                                self.scanner_tab, "Vulnerability Scanner")
                                            logger.info(
                                                "Scanner tab added successfully")

                                            # Tool Management Tab
                                            self.tool_tab = ToolTab(
                                                tool_manager=self.tool_manager
                                            )  # Pass tool_manager as a keyword argument
                                            self.tabs.add_tab(
                                                self.tool_tab, "Tool Management")
                                            logger.info(
                                                "Tool Management tab added successfully")

                                            except Exception as e:
                                                logger.error(
                                                    f"Error setting up tabs: {str(e)}", exc_info=True)
                                                raise

                                                def show_login(self):
                                                    """Show login dialog and return True if login successful"""
                                                    dialog = LoginDialog(
                                                        self.auth_manager)
                                                    if dialog.exec():
                                                        self.user_token = dialog.get_token()
                                                        result = self.auth_manager.verify_token(
                                                            self.user_token)
                                                        if result["status"] == "success":
                                                            self.current_user = result["payload"]["username"]
                                                            self.user_role = result["payload"]["role"]
                                                            self.log_display.append(
                                                                f"Logged in as: {self.current_user} (Role: {self.user_role})"
                                                            )
                                                        return True
                                                    return False

                                                    def load_preferences(self):
                                                        """Load user preferences"""
                                                        try:
                                                            with open("preferences.json", "r", encoding="utf-8") as f:
                                                                self.preferences = json.load(
                                                                    f)
                                                                except FileNotFoundError:
                                                                    self.preferences = {}

                                                                    def save_preferences(self):
                                                                        """Save user preferences"""
                                                                        with open("preferences.json", "w", encoding="utf-8") as f:
                                                                            json.dump(
                                                                                self.preferences, f)

                                                                            def create_tools_directory(self):
                                                                                """Create tools directory if it doesn't exist"""
                                                                                tools_dir = os.path.join(os.path.dirname(
                                                                                    os.path.dirname(__file__)), "tools")
                                                                                if not os.path.exists(tools_dir):
                                                                                    os.makedirs(
                                                                                        tools_dir)
                                                                                    logger.info(
                                                                                        f"Created tools directory at {tools_dir}")

                                                                                    def close_event(self, _event):
                                                                                        """Handle application close event"""
                                                                                        self.save_preferences()
                                                                                        event.accept()

                                                                                        def main():
                                                                                            try:
                                                                                                # Initialize application
                                                                                                app = QApplication(
                                                                                                    sys.argv)
                                                                                                app.set_style(
                                                                                                    "Fusion")

                                                                                                # Create and show main window
                                                                                                window = IntegratedApp()
                                                                                                window.show()

                                                                                                # Start event loop
                                                                                                sys.exit(
                                                                                                    app.exec())

                                                                                                except Exception as e:
                                                                                                    logger.error(
                                                                                                        f"Application error: {str(e)}", exc_info=True)
                                                                                                    sys.exit(
                                                                                                        1)

                                                                                                    if __name__ == "__main__":
                                                                                                        main()
