from app.services.website_scanner import WebsiteScanner
from app.services.wayback_machine_integration import WaybackMachineIntegration
from app.services.vulnerability_scanner import VulnerabilityScanner
from app.services.user_auth import UserAuth
from app.services.tool_manager import ToolManager
from app.services.shodan_integration import ShodanIntegration
from app.services.scope_manager import ScopeManager
from app.services.scanning_profiles import ScanningProfiles
from app.services.notification import NotificationSystem
from app.services.database import DatabaseManager
from app.services.collaboration_system import CollaborationSystem
from app.services.chat_system import ChatSystem
from app.services.analytics_system import AnalyticsSystem
from app.services import initialize_services
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from dataclasses import dataclass
import sys
import logging
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QTabWidget
k = 10
directory = ""
ai_system = None
message = ""
tools = []
templates = []


# Initialize logger
logger = logging.get_logger(__name__)
logger.set_level(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.set_formatter(formatter)
logger.add_handler(handler)


@dataclass
   class BugHunterApp:
    """
    Main application
        def __init__(self):
        class for BugHunter.
        Initializes and manages all components and services.
        """

       def __init__(self):
        """
        Initialize the BugHunter application.
        Sets up the QApplication, logging, and core managers.
        """
        self.app = QApplication(sys.argv)
        self.logger = logging.get_logger("BugHunter.App")

        # Enable High DPI support
        QCoreApplication.set_attribute(
            Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        QCoreApplication.set_attribute(
            Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        self.db_manager = DatabaseManager()
        self.auth_manager = UserAuth()
        self.tool_manager = ToolManager()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.ai_system = AISystem()
        self.collaboration_system = CollaborationSystem()
        self.analytics_system = AnalyticsSystem()
        self.notification_system = NotificationSystem()
        self.chat_system = ChatSystem()
        self.scope_manager = ScopeManager()
        self.role_manager = RoleManager()
        self.scanning_profiles = ScanningProfiles()
        self.vulnerability_database = VulnerabilityDatabase()
        self.wayback_integration = WaybackMachineIntegration()
        self.shodan_integration = ShodanIntegration()
        self.website_scanner = WebsiteScanner(self.kb)

           try:
            self._create_directories()
            self._setup_application_style()
            self.db_manager.initialize()
            self._initialize_services()
            self._load_configurations()

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
                shodan_integration=self.shodan_integration,
                website_scanner=self.website_scanner,  # Pass the website scanner
            )

            self.logger.info("Application initialized successfully")
        return True

           except Exception as e:
            self.logger.error(
                f"Failed to initialize application: {str(e)}", exc_info=True
            )
            QMessageBox.critical(
                None,
                "Initialization Error",
                f"Failed to initialize application: {str(e)}",
            )
        return False

           def _create_directories(self):
            """
                Create necessary application directories.
                """
            directories = [
                "logs",
                "data",
                "reports",
                "tools",
                "cache",
                "config",
                "temp",
                "downloads",
                "uploads",
                "backups",
                "profiles",
                "templates",
                "assets/icons",
                "assets/styles",
                "assets/templates",
            ]

               for directory in directories:
                os.makedirs(directory, exist_ok=True)
                self.logger.info("Application directories created")

                   def _initialize_services(self):
                    """
                        Initialize all application services.
                        """
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

                        self.logger.info(
                            "All services initialized successfully")

                           except Exception as e:
                            self.logger.error(
                                f"Service initialization failed: {str(e)}")
                            raise

                               def _load_configurations(self):
                                """
                                    Load all configuration files.
                                    """
                                   try:
                                        # Load main configurations
                                    self.config_manager.load_config(
                                        "config.json")
                                    self.config_manager.load_config(
                                        "config/system_config.json")

                                    # Load tool configurations
                                    self.config_manager.load_config(
                                        "tools.yml")
                                    self.config_manager.load_config(
                                        "nuclei.yaml")
                                    self.config_manager.load_config(
                                        "amass.ini")

                                    # Load scanning profiles
                                    self.scanning_profiles.load_profiles(
                                        "scanning_profiles.json")

                                    self.logger.info(
                                        "All configurations loaded successfully")

                                       except Exception as e:
                                        self.logger.error(
                                            f"Configuration loading failed: {str(e)}")
                                        raise

                                           def _setup_application_style(self):
                                            """
                                                Setup application-wide style and theme.
                                                """
                                            self.app.set_style("Fusion")
                                            self.app.set_application_name(
                                                "BugHunter")
                                            self.app.set_application_version(
                                                "2.0.0")

                                            # Load and apply application stylesheet
                                               try:
                                                with open(
                                                    "assets/styles/dark_theme.qss", "r", encoding="utf-8"
                                                ) as style_file:
                                                    self.app.set_styleSheet(
                                                        style_file.read())
                                                       except Exception as e:
                                                        self.logger.warning(
                                                            f"Could not load stylesheet: {str(e)}")

                                                           def run(self):
                                                            """
                                                                Run the application.
                                                                """
                                                               try:
                                                                    if not self.initialize():
                                                                return 1

                                                                self.window.show()
                                                            return self.app.exec()

                                                               except Exception as e:
                                                                self.logger.error(
                                                                    f"Application error: {str(e)}", exc_info=True)
                                                                QMessageBox.critical(
                                                                    None, "Fatal Error", f"Application error: {str(e)}")
                                                            return 1

                                                               def main():
                                                                app = QApplication(
                                                                    sys.argv)

                                                                # Create the main tab widget
                                                                tab_widget = QTabWidget()

                                                                # Initialize services and set up tabs
                                                                initialize_services(
                                                                    tab_widget)

                                                                # Show the main tab widget
                                                                tab_widget.show()

                                                                # Initialize your application here
                                                                wayback_machine_integration = WaybackMachineIntegration()
                                                                notification_system = NotificationSystem()

                                                                # ...other initialization code...

                                                                sys.exit(
                                                                    app.exec_())

                                                                   if __name__ == "__main__":
                                                                    main()
