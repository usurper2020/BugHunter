"""
Main entry point for the BugHunter application.
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import services
from services.vulnerability_scanner import VulnerabilityScanner
from services.ai_system import AISystem
from services.user_auth import UserAuth
from services.login_dialog import LoginDialog
from tool_manager import ToolManager

# Import tabs
from tabs.ai_chat_tab import AIChatTab
from tabs.nuclei_tab import NucleiTab
from tabs.amass_tab import AmassTab
from tabs.scanner_tab import ScannerTab
from tabs.tool_manager_tab import ToolManagerTab

class MainWindow(QMainWindow):
    """Main window of the BugHunter application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Bug Hunter")
        self.setMinimumSize(1200, 800)
        
        # Initialize logger
        self.logger = logging.getLogger('BugHunter.MainWindow')
        
        # Initialize services
        self.auth_manager = UserAuth()
        self.tool_manager = ToolManager()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.ai_system = AISystem()
        
        # Show login dialog
        if not self.show_login():
            sys.exit()
            
        # Create required directories
        self.create_required_directories()
        
        # Initialize UI
        self.setup_ui()
        
        self.logger.info("Application initialization completed")

    def setup_ui(self):
        """Set up the user interface."""
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
        """)

    def setup_tabs(self):
        """Set up application tabs."""
        try:
            # AI Chat Tab
            self.ai_chat_tab = AIChatTab(ai_system=self.ai_system)
            self.tab_widget.addTab(self.ai_chat_tab, "AI Assistant")

            # Scanner Tab
            self.scanner_tab = ScannerTab(scanner=self.vulnerability_scanner)
            self.tab_widget.addTab(self.scanner_tab, "Vulnerability Scanner")

            # Tool Management Tab
            self.tool_tab = ToolManagerTab(tool_manager=self.tool_manager)
            self.tab_widget.addTab(self.tool_tab, "Tool Management")

            # Amass Tab
            self.amass_tab = AmassTab(scanner=self.vulnerability_scanner)
            self.tab_widget.addTab(self.amass_tab, "Amass")

            # Nuclei Tab
            self.nuclei_tab = NucleiTab(scanner=self.vulnerability_scanner)
            self.tab_widget.addTab(self.nuclei_tab, "Nuclei")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error setting up tabs: {str(e)}"
            )
            raise

    def show_login(self):
        """Show login dialog."""
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
        """Create required directories."""
        try:
            directories = ['logs', 'data', 'reports', 'tools', 'cache', 'config']
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
            self.logger.info("Required directories created successfully")
        except Exception as e:
            self.logger.error(f"Error creating directories: {str(e)}")
            raise

def main():
    """Application entry point."""
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
