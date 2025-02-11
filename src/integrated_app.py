import sys
import json
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLineEdit, QTextEdit, QTabWidget, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from services.tool_manager import ToolManager
from services.ai_integration import AIIntegration
from services.ai_training import AITraining
from services.scope_manager import ScopeManager
from services.shodan_integration import ShodanIntegration
from services.wayback_machine_integration import WaybackMachineIntegration
from services.report_generator import ReportGenerator
from services.vulnerability_scanner import VulnerabilityScanner
from services.scanning_profiles import ScanningProfiles
from services.vulnerability_database import VulnerabilityDatabase
from services.collaboration import Collaboration
from services.notification import Notification
from services.user_auth import UserAuth
from services.login_dialog import LoginDialog
from services.role_manager import RoleManager
from services.user_management_dialog import UserManagementDialog
from services.analytics_system import AnalyticsSystem
from services.collaboration_system import CollaborationSystem
from services.collaboration_dialog import CollaborationDialog
from services.contribution_dialog import ContributionDialog
from services.contribution_system import ContributionSystem

from tabs.ai_chat_tab import AIChatTab
from tabs.tool_tab import ToolTab
from scanner_tab import ScannerTab
from core import config, logger_config

logger = logger_config.get_logger(__name__)

class IntegratedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bug Hunter - Security Testing Tool")
        self.setMinimumSize(1200, 800)

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
        self.initUI()
        self.load_preferences()

    def init_components(self):
        """Initialize all system components"""
        self.tool_manager = ToolManager()
        self.ai_integration = AIIntegration()
        self.ai_training = AITraining()
        self.scope_manager = ScopeManager()
        self.shodan_integration = ShodanIntegration(config.get('SHODAN_API_KEY', ''))
        self.wayback_integration = WaybackMachineIntegration()
        self.report_generator = ReportGenerator()
        self.scanner = VulnerabilityScanner()
        self.profiles_manager = ScanningProfiles()
        self.vulnerability_database = VulnerabilityDatabase()
        self.collaboration_system = CollaborationSystem()
        self.analytics_system = AnalyticsSystem()
        self.contribution_system = ContributionSystem()

    def init_base_ui(self):
        """Initialize base UI elements needed before login"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add header
        header = QLabel("Bug Hunter")
        header.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2196f3; margin: 10px;")
        main_layout.addWidget(header)

        # Create log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.append("Please log in to continue...")
        main_layout.addWidget(self.log_display)

    def initUI(self):
        """Initialize the main UI after successful login"""
        # Create main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Add the log display to the new layout
        old_widget = self.log_display.parent()
        if old_widget:
            old_widget.layout().removeWidget(self.log_display)
        self.log_display.setMaximumHeight(150)
        main_layout.addWidget(self.log_display)

        # Create and add tabs
        self.setup_tabs()

        # Set window style
        self.setStyleSheet("""
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
        """)

    def setup_tabs(self):
        """Set up all application tabs"""
        try:
            # AI Assistant Tab
            self.ai_chat_tab = AIChatTab()
            self.tabs.addTab(self.ai_chat_tab, "AI Assistant")
            logger.info("AI Assistant tab added successfully")

            # Scanner Tab
            self.scanner_tab = ScannerTab()
            self.tabs.addTab(self.scanner_tab, "Vulnerability Scanner")
            logger.info("Scanner tab added successfully")

            # Tool Management Tab
            self.tool_tab = ToolTab()
            self.tabs.addTab(self.tool_tab, "Tool Management")
            logger.info("Tool Management tab added successfully")

            # Other tabs can be added here...

        except Exception as e:
            logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)
            raise

    def show_login(self):
        """Show login dialog and return True if login successful"""
        dialog = LoginDialog(self.auth_manager)
        if dialog.exec():
            self.user_token = dialog.get_token()
            result = self.auth_manager.verify_token(self.user_token)
            if result['status'] == 'success':
                self.current_user = result['payload']['username']
                self.user_role = result['payload']['role']
                self.log_display.append(f"Logged in as: {self.current_user} (Role: {self.user_role})")
                return True
        return False

    def load_preferences(self):
        """Load user preferences"""
        try:
            with open('preferences.json', 'r') as f:
                self.preferences = json.load(f)
        except FileNotFoundError:
            self.preferences = {}

    def save_preferences(self):
        """Save user preferences"""
        with open('preferences.json', 'w') as f:
            json.dump(self.preferences, f)

    def create_tools_directory(self):
        """Create tools directory if it doesn't exist"""
        tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools')
        if not os.path.exists(tools_dir):
            os.makedirs(tools_dir)
            logger.info(f"Created tools directory at {tools_dir}")

    def closeEvent(self, event):
        """Handle application close event"""
        self.save_preferences()
        event.accept()

def main():
    try:
        # Initialize application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Create and show main window
        window = IntegratedApp()
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
