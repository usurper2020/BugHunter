import sys
import os
import json
import asyncio
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QTabWidget, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from services import (
    SecuritySystem,
    IntegrationManager,
    AISystem,
    CollaborationSystem,
    ConfigManager
)
from services.user_auth import UserAuth
from services.login_dialog import LoginDialog
from services.tool_manager import ToolManager
from services.vulnerability_scanner import VulnerabilityScanner

from tabs import (
    AIChatTab,
    ToolTab,
    ScannerTab,
    AmassTab,
    NucleiTab,
    ToolManagerTab
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bug Hunter")
        self.setMinimumSize(1200, 800)

        # Initialize configuration and logging
        self.config_manager = ConfigManager()
        self.logger = logging.getLogger('BugHunter.MainWindow')
        
        # Initialize authentication with config
        self.auth_manager = UserAuth()
        self.user_token = None
        self.current_user = None
        self.user_role = None

        # Show login dialog
        if not self.show_login():
            sys.exit()

        # Initialize core services with config
        self.tool_manager = ToolManager(self.config_manager.get_tool_config())
        self.vulnerability_scanner = VulnerabilityScanner()
        
        # Initialize integrated systems with config
        self.security_system = SecuritySystem(self.config_manager.get_security_config())
        self.integration_manager = IntegrationManager(self.config_manager.get_integration_config())
        self.ai_system = AISystem(self.config_manager.get_ai_config())
        self.collaboration_system = CollaborationSystem(self.config_manager.get_collaboration_config())
        
        # Create required directories and initialize systems
        self.create_required_directories()
        self.initialize_systems()
        
        # Initialize UI
        self.setup_ui()
        
        self.logger.info("Application initialization completed")

    def setup_ui(self):
        """Initialize the user interface"""
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add header
        header = QLabel("Bug Hunter")
        header.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2196f3; margin: 10px;")
        layout.addWidget(header)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add tabs
        self.setup_tabs()

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #1e1e1e;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #2196f3;
            }
            QTabBar::tab:hover:!selected {
                background: #1976d2;
            }
            QTextEdit, QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #666666;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid #666666;
                border-right: 5px solid #666666;
                border-top: 5px solid #ffffff;
                width: 0;
                height: 0;
            }
            QProgressBar {
                border: 1px solid #333333;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196f3;
            }
        """)

    def setup_tabs(self):
        """Set up application tabs"""
        try:
            # AI Chat Tab with integrated AI system
            self.ai_chat_tab = AIChatTab(ai_system=self.ai_system)
            self.tab_widget.addTab(self.ai_chat_tab, "AI Assistant")

            # Scanner Tab
            self.scanner_tab = ScannerTab()
            self.tab_widget.addTab(self.scanner_tab, "Vulnerability Scanner")

            # Tool Management Tab
            self.tool_tab = ToolTab()
            self.tab_widget.addTab(self.tool_tab, "Tool Management")

            # Amass Tab
            self.amass_tab = AmassTab()
            self.tab_widget.addTab(self.amass_tab, "Amass")

            # Nuclei Tab
            self.nuclei_tab = NucleiTab()
            self.tab_widget.addTab(self.nuclei_tab, "Nuclei")

            # Tool Manager Tab
            self.tool_manager_tab = ToolManagerTab()
            self.tab_widget.addTab(self.tool_manager_tab, "Tool Manager")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error setting up tabs: {str(e)}"
            )
            raise

    def show_login(self) -> bool:
        """Show login dialog and return True if login successful"""
        dialog = LoginDialog(self.auth_manager)
        if dialog.exec():
            self.user_token = dialog.get_token()
            result = self.auth_manager.verify_token(self.user_token)
            if result['status'] == 'success':
                self.current_user = result['payload']['username']
                self.user_role = result['payload']['role']
                return True
        return False

    def create_required_directories(self):
        """Create required directories"""
        try:
            directories = ['logs', 'data', 'reports', 'tools', 'cache', 'config']
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
            self.logger.info("Required directories created successfully")
        except Exception as e:
            self.logger.error(f"Error creating directories: {str(e)}")
            raise
            
    def initialize_systems(self):
        """Initialize all integrated systems"""
        try:
            # Initialize security system
            self.security_system.initialize()
            self.logger.info("Security system initialized")
            
            # Initialize integration manager
            self.integration_manager.initialize_integrations()
            self.logger.info("Integration manager initialized")
            
            # Initialize AI system
            self.ai_system.initialize()
            self.logger.info("AI system initialized")
            
            # Initialize collaboration system
            self.collaboration_system.initialize()
            self.logger.info("Collaboration system initialized")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "System Initialization Error",
                f"Error initializing systems: {str(e)}"
            )
            raise

def main():
    try:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/bughunter.log'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger('BugHunter')
        logger.info("Starting Bug Hunter application")
        
        # Initialize application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"Application error: {str(e)}"
        )
        sys.exit(1)

if __name__ == '__main__':
    main()
