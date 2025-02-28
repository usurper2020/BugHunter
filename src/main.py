"""
Entry point for the BugHunter application.
Handles initialization of core services and GUI components.
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox

from src.gui.main_window import MainWindow
from src.gui.login_dialog import LoginDialog
from src.gui.theme import apply_dark_theme

from src.services.simple_auth import SimpleAuth
from src.services.config_manager import ConfigManager
from src.services.notification import Notification
from src.services.tool_manager import ToolManager
from src.services.vulnerability_scanner import VulnerabilityScanner
from src.services.ai_system import AISystem
from src.services.collaboration_system import CollaborationSystem
from src.services.analytics_system import AnalyticsSystem
from src.services.scope_manager import ScopeManager
from src.services.role_manager import RoleManager
from src.services.scanning_profiles import ScanningProfiles
from src.services.vulnerability_database import VulnerabilityDatabase
from src.services.wayback_machine_integration import WaybackMachineIntegration
from src.services.shodan_integration import ShodanIntegration

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bughunter.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('BugHunter')

def initialize_services():
    """Initialize all required services"""
    services = {}
    
    # Initialize core services
    services['config_manager'] = ConfigManager()
    services['auth_manager'] = SimpleAuth()
    services['notification_system'] = Notification(services['auth_manager'])

    services['tool_manager'] = ToolManager(services['config_manager'])
    services['vulnerability_scanner'] = VulnerabilityScanner(services['config_manager'])
    services['ai_system'] = AISystem(services['config_manager'])
    services['collaboration_system'] = CollaborationSystem(services['config_manager'])
    services['analytics_system'] = AnalyticsSystem(services['config_manager'])
    services['scope_manager'] = ScopeManager(services['config_manager'])
    services['role_manager'] = RoleManager(services['config_manager'])
    services['scanning_profiles'] = ScanningProfiles(services['config_manager'])
    services['vulnerability_database'] = VulnerabilityDatabase(services['config_manager'])
    services['wayback_integration'] = WaybackMachineIntegration(services['config_manager'])
    services['shodan_integration'] = ShodanIntegration(services['config_manager'])
    
    return services

def main():
    """Main entry point of the application"""
    # Initialize logging
    logger = setup_logging()
    logger.info("Starting BugHunter application")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("BugHunter")
    apply_dark_theme(app)

    # Initialize services
    services = initialize_services()
    logger.info("Services initialized successfully")
    
    # Show login dialog
    login_dialog = LoginDialog(services['auth_manager'])
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        try:
            # Create and show main window
            main_window = MainWindow(

            config_manager=services['config_manager'],
            auth_manager=services['auth_manager'],
            tool_manager=services['tool_manager'],
            vulnerability_scanner=services['vulnerability_scanner'],
            ai_system=services['ai_system'],
            collaboration_system=services['collaboration_system'],
            analytics_system=services['analytics_system'],
            notification_system=services['notification_system'],
            scope_manager=services['scope_manager'],
            role_manager=services['role_manager'],
            scanning_profiles=services['scanning_profiles'],
            vulnerability_database=services['vulnerability_database'],
            wayback_integration=services['wayback_integration'],
            shodan_integration=services['shodan_integration']
            )
            main_window.show()
            logger.info("Main window displayed")
            
            # Start the application event loop
            sys.exit(app.exec())
        except Exception as e:
            logger.error(f"Failed to initialize main window: {str(e)}")
            QMessageBox.critical(None, "Fatal Error", 
                f"Failed to initialize application: {str(e)}")
            sys.exit(1)

    else:
        logger.info("Login failed, closing application")
        sys.exit(1)

if __name__ == "__main__":
    main()
