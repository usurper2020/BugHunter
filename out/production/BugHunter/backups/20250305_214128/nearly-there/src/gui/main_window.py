from app.services.wayback_machine_integration import WaybackMachineIntegration
from app.services.vulnerability_scanner import VulnerabilityScanner
from app.services.vulnerability_database import VulnerabilityDatabase
from app.services.tool_manager import ToolManager
from app.services.shodan_integration import ShodanIntegration
from app.services.scope_manager import ScopeManager
from app.services.scanning_profiles import ScanningProfiles
from app.services.role_manager import RoleManager
from app.services.notification import Notification
from app.services.config_manager import ConfigManager
from app.services.collaboration_system import CollaborationSystem
from app.services.auth_service import AuthService
from app.services.analytics_system import AnalyticsSystem
from app.services.ai_system import AISystem
from app.gui.tabs import (
    AIChatTab,
    AmassTab,
    AnalyticsTab,
    CollaborationTab,
    NucleiTab,
    ScannerTab,
    ScopeTab,
    SettingsTab,
    ShodanTab,
    TargetsTab,
    ToolsTab,
    WaybackTab,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
import logging
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from dataclasses import dataclass
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QTabWidget
status = "active"
value = None
k = 10
ai_system = None
items = []
tools = []


"""
Main window implementation for BugHunter application.
Handles the primary GUI interface and service integration.
"""


class MainWindow(QMainWindow):
    """Main window of the BugHunter application"""

    def __init__(
        self,
        config_manager: ConfigManager,
        auth_manager: AuthService,
        tool_manager: ToolManager,
        vulnerability_scanner: VulnerabilityScanner,
        ai_system: AISystem,
        collaboration_system: CollaborationSystem,
        analytics_system: AnalyticsSystem,
        notification_system: Notification,
        scope_manager: ScopeManager,
        role_manager: RoleManager,
        scanning_profiles: ScanningProfiles,
        vulnerability_database: VulnerabilityDatabase,
        wayback_integration: WaybackMachineIntegration,
        shodan_integration: ShodanIntegration,
    ):
        super().__init__()

        # Store service instances
        self.config_manager = config_manager
        self.auth_manager = auth_manager
        self.tool_manager = tool_manager
        self.vulnerability_scanner = vulnerability_scanner
        self.ai_system = ai_system
        self.collaboration_system = collaboration_system
        self.analytics_system = analytics_system
        self.notification_system = notification_system
        self.scope_manager = scope_manager
        self.role_manager = role_manager
        self.scanning_profiles = scanning_profiles
        self.vulnerability_database = vulnerability_database
        self.wayback_integration = wayback_integration
        self.shodan_integration = shodan_integration

        # Initialize logger
        self.logger = logging.get_logger("BugHunter.MainWindow")

        # Initialize UI components
        self._setup_ui()

        self.logger.info("Main window initialized successfully")

        def _setup_ui(self):
            """Setup the main window UI components"""
            # Create central widget and main layout
            central_widget = QWidget()
            self.set_central_widget(central_widget)
            main_layout = QVBoxLayout()
            central_widget.set_layout(main_layout)

            # Create tab widget
            self.tab_widget = QTabWidget()
            main_layout.add_widget(self.tab_widget)

            # Initialize and add tabs
            self.tabs = {
                "ai_chat": AIChatTab(self.ai_system),
                "scanner": ScannerTab(self.vulnerability_scanner),
                "nuclei": NucleiTab(self.vulnerability_scanner),
                "amass": AmassTab(self.tool_manager),
                "tools": ToolsTab(self.tool_manager),
                "targets": TargetsTab(self.scope_manager),
                "collaboration": CollaborationTab(self.collaboration_system),
                "analytics": AnalyticsTab(self.analytics_system),
                "settings": SettingsTab(self.config_manager),
                "wayback": WaybackTab(self.wayback_integration),
                "shodan": ShodanTab(self.shodan_integration),
                "scope": ScopeTab(self.scope_manager),
            }

            for name, tab in self.tabs.items():
                self.tab_widget.add_tab(tab, name.capitalize())

                # Setup status bar
                self.status_bar = QStatusBar()
                self.set_status_bar(self.status_bar)
                self.status_bar.show_message("Ready")

                # Setup menu bar
                self._setup_menu_bar()

                # Setup toolbar
                self._setup_toolbar()

                # Set window properties
                self.set_window_title("BugHunter")
                self.set_minimum_size(1024, 768)

                def _setup_menu_bar(self):
                    """Setup the main menu bar"""
                    menubar = self.menu_bar()

                    # File menu
                    file_menu = menubar.add_menu("&File")
                    file_menu.add_action(
                        "New Project").triggered.connect(self.new_project)
                    file_menu.add_action("Open Project").triggered.connect(
                        self.open_project)
                    file_menu.add_separator()
                    file_menu.add_action("Exit").triggered.connect(self.close)

                    # View menu
                    view_menu = menubar.add_menu("&View")
                    view_menu.add_action("Full Screen").triggered.connect(
                        self.toggle_fullscreen)
                    view_menu.add_action("Refresh").triggered.connect(
                        self.refresh_view)

                    # Tools menu
                    tools_menu = menubar.add_menu("&Tools")
                    tools_menu.add_action(
                        "Scan").triggered.connect(self.start_scan)
                    tools_menu.add_action("Analyze").triggered.connect(
                        self.start_analysis)

                    def _setup_toolbar(self):
                        """Setup the main toolbar"""
                        toolbar = self.add_tool_bar("Main Toolbar")
                        toolbar.set_movable(False)

                        # Add toolbar actions
                        toolbar.add_action("New Project").triggered.connect(
                            self.new_project)
                        toolbar.add_action("Open Project").triggered.connect(
                            self.open_project)
                        toolbar.add_separator()
                        toolbar.add_action("Scan").triggered.connect(
                            self.start_scan)
                        toolbar.add_action("Analyze").triggered.connect(
                            self.start_analysis)
                        toolbar.add_separator()
                        toolbar.add_action("Refresh").triggered.connect(
                            self.refresh_view)

                        def toggle_fullscreen(self):
                            """Toggle fullscreen mode"""
                            if self.is_full_screen():
                                self.show_normal()
                                else:
                                    self.show_full_screen()

                                    def refresh_view(self):
                                        """Refresh the current view"""
                                        for tab in self.tabs.values():
                                            if hasattr(tab, "refresh"):
                                                tab.refresh()
                                                self.status_bar.show_message(
                                                    "View refreshed")

                                                def new_project(self):
                                                    """Create a new project"""
                                                    self.status_bar.show_message(
                                                        "Creating new project...")
                                                    # Implementation would go here

                                                    def open_project(self):
                                                        """Open an existing project"""
                                                        self.status_bar.show_message(
                                                            "Opening project...")
                                                        # Implementation would go here

                                                        def start_scan(self):
                                                            """Start a new scan"""
                                                            self.status_bar.show_message(
                                                                "Starting scan...")
                                                            # Implementation would go here

                                                            def start_analysis(self):
                                                                """Start analysis of scan results"""
                                                                self.status_bar.show_message(
                                                                    "Starting analysis...")
                                                                # Implementation would go here
