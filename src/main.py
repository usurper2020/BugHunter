"""
Main entry point for the BugHunter application.
Enhanced version with integrated security tools and utilities.
"""

import sys
import os
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QCoreApplication

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Core imports
from src.gui.main_window import MainWindow
from services.config_manager import ConfigManager
from services.database import DatabaseManager
from services.user_auth import UserAuth
from services.tool_manager import ToolManager
from services.vulnerability_scanner import VulnerabilityScanner
from services.ai_system import AISystem
from services.collaboration_system import CollaborationSystem
from services.analytics_system import AnalyticsSystem
from services.wayback_machine_integration import WaybackMachineIntegration
from services.shodan_integration import ShodanIntegration

# Additional service imports
from services.notification import NotificationSystem
from services.chat_system import ChatSystem
from services.scope_manager import ScopeManager
from services.role_manager import RoleManager
from services.scanning_profiles import ScanningProfiles
from services.vulnerability_database import VulnerabilityDatabase

# Configuration
from logger_config import logger_config

class BugHunterApp:
    """Enhanced BugHunter application class with integrated security tools"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.logger = logging.getLogger('BugHunter.App')
        
        # Enable High DPI support
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        
        # Initialize core managers
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        self.auth_manager = UserAuth()
        
        # Initialize security tools
        self.tool_manager = ToolManager()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.ai_system = AISystem()
        self.collaboration_system = CollaborationSystem()
        self.analytics_system = AnalyticsSystem()
        
        # Initialize additional services
        self.notification_system = NotificationSystem()
        self.chat_system = ChatSystem()
        self.scope_manager = ScopeManager()
        self.role_manager = RoleManager()
        self.scanning_profiles = ScanningProfiles()
        self.vulnerability_database = VulnerabilityDatabase()
        self.wayback_integration = WaybackMachineIntegration()
        self.shodan_integration = ShodanIntegration()
    
    def initialize(self):
        """Initialize the application and all its components"""
        try:
            # Create required directories
            self._create_directories()
            
            # Setup application style
            self._setup_application_style()
            
            # Initialize database
            self.db_manager.initialize()
            
            # Initialize all services
            self._initialize_services()
            
            # Load configurations
            self._load_configurations()
            
            # Create main window with all services
            self.window = MainWindow(
                config_manager=self.config_manager,
                db_manager=self.db_manager,
                auth_manager=self.auth_manager,
                tool_manager=self.tool_manager,
                vulnerability_scanner=self.vulnerability_scanner,
                ai_system=self.ai_system,
                collaboration_system=self.collaboration_system,
                analytics_system=self.analytics_system,
                notification_system=self.notification_system,
                chat_system=self.chat_system,
                scope_manager=self.scope_manager,
                role_manager=self.role_manager,
                scanning_profiles=self.scanning_profiles,
                vulnerability_database=self.vulnerability_database,
                wayback_integration=self.wayback_integration,
                shodan_integration=self.shodan_integration
            )
            
            self.logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {str(e)}", exc_info=True)
            QMessageBox.critical(
                None,
                "Initialization Error",
                f"Failed to initialize application: {str(e)}"
            )
            return False
    
    def _create_directories(self):
        """Create necessary application directories"""
        directories = [
            'logs',
            'data',
            'reports',
            'tools',
            'cache',
            'config',
            'temp',
            'downloads',
            'uploads',
            'backups',
            'profiles',
            'templates',
            'assets/icons',
            'assets/styles',
            'assets/templates'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        self.logger.info("Application directories created")
    
    def _initialize_services(self):
        """Initialize all application services"""
        try:
            # Initialize core services
            self.ai_system.initialize()
            self.collaboration_system.initialize()
            self.analytics_system.initialize()
            
            # Initialize security tools
            self.tool_manager.initialize()
            self.vulnerability_scanner.initialize()
            self.vulnerability_database.initialize()
            
            # Initialize additional services
            self.notification_system.initialize()
            self.chat_system.initialize()
            self.scope_manager.initialize()
            self.role_manager.initialize()
            self.scanning_profiles.initialize()
            self.wayback_integration.initialize()
            self.shodan_integration.initialize()
            
            self.logger.info("All services initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Service initialization failed: {str(e)}")
            raise
    
    def _load_configurations(self):
        """Load all configuration files"""
        try:
            # Load main configurations
            self.config_manager.load_config('config.json')
            self.config_manager.load_config('config/system_config.json')
            
            # Load tool configurations
            self.config_manager.load_config('tools.yml')
            self.config_manager.load_config('nuclei.yaml')
            self.config_manager.load_config('amass.ini')
            
            # Load scanning profiles
            self.scanning_profiles.load_profiles('scanning_profiles.json')
            
            self.logger.info("All configurations loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Configuration loading failed: {str(e)}")
            raise
    
    def _setup_application_style(self):
        """Setup application-wide style and theme"""
        self.app.setStyle('Fusion')
        self.app.setApplicationName("BugHunter")
        self.app.setApplicationVersion("2.0.0")
        
        # Load and apply application stylesheet
        try:
            with open('assets/styles/dark_theme.qss', 'r') as style_file:
                self.app.setStyleSheet(style_file.read())
        except Exception as e:
            self.logger.warning(f"Could not load stylesheet: {str(e)}")
    
    def run(self):
        """Run the application"""
        try:
            if not self.initialize():
                return 1
                
            self.window.show()
            return self.app.exec()
            
        except Exception as e:
            self.logger.error(f"Application error: {str(e)}", exc_info=True)
            QMessageBox.critical(
                None,
                "Fatal Error",
                f"Application error: {str(e)}"
            )
            return 1

def main():
    """Application entry point"""
    try:
        # Setup logging
        logger_config.setup_logging()
        logger = logging.getLogger('BugHunter')
        logger.info("Starting BugHunter application")
        
        # Create and run application
        app = BugHunterApp()
        exit_code = app.run()
        
        logger.info(f"Application exiting with code: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"Fatal application error: {str(e)}"
        )
        sys.exit(1)

if __name__ == '__main__':
    main()
