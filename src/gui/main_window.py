"""
Main window implementation for BugHunter application.
Handles the primary GUI interface and service integration.
"""

import logging
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStatusBar, QMenuBar, QToolBar
from PyQt6.QtCore import Qt

from src.gui.tabs import (
    AIChatTab,
    ScannerTab,
    NucleiTab,
    AmassTab,
    ToolsTab,
    TargetsTab,
    CollaborationTab,
    AnalyticsTab,
    SettingsTab,
    WaybackTab,
    ShodanTab,
    ScopeTab
)

from src.services.config_manager import ConfigManager
from src.services.auth_service import AuthService
from src.services.tool_manager import ToolManager
from src.services.vulnerability_scanner import VulnerabilityScanner
from src.services.ai_system import AISystem
from src.services.collaboration_system import CollaborationSystem
from src.services.analytics_system import AnalyticsSystem
from src.services.notification import Notification
from src.services.scope_manager import ScopeManager
from src.services.role_manager import RoleManager
from src.services.scanning_profiles import ScanningProfiles
from src.services.vulnerability_database import VulnerabilityDatabase
from src.services.wayback_machine_integration import WaybackMachineIntegration
from src.services.shodan_integration import ShodanIntegration

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
        shodan_integration: ShodanIntegration
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
        self.logger = logging.getLogger('BugHunter.MainWindow')
        
        # Initialize UI components
        self._setup_ui()
        
        self.logger.info("Main window initialized successfully")

    def _setup_ui(self):
        """Setup the main window UI components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Initialize and add tabs
        self.tabs = {
            'ai_chat': AIChatTab(self.ai_system),
            'scanner': ScannerTab(self.vulnerability_scanner),
            'nuclei': NucleiTab(self.vulnerability_scanner),
            'amass': AmassTab(self.tool_manager),
            'tools': ToolsTab(self.tool_manager),
            'targets': TargetsTab(self.scope_manager),
            'collaboration': CollaborationTab(self.collaboration_system),
            'analytics': AnalyticsTab(self.analytics_system),
            'settings': SettingsTab(self.config_manager),
            'wayback': WaybackTab(self.wayback_integration),
            'shodan': ShodanTab(self.shodan_integration),
            'scope': ScopeTab(self.scope_manager)
        }
        
        for name, tab in self.tabs.items():
            self.tab_widget.addTab(tab, name.capitalize())

        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Setup menu bar
        self._setup_menu_bar()

        # Setup toolbar
        self._setup_toolbar()

        # Set window properties
        self.setWindowTitle("BugHunter")
        self.setMinimumSize(1024, 768)

    def _setup_menu_bar(self):
        """Setup the main menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("New Project").triggered.connect(self.new_project)
        file_menu.addAction("Open Project").triggered.connect(self.open_project)
        file_menu.addSeparator()
        file_menu.addAction("Exit").triggered.connect(self.close)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction("Full Screen").triggered.connect(self.toggle_fullscreen)
        view_menu.addAction("Refresh").triggered.connect(self.refresh_view)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        tools_menu.addAction("Scan").triggered.connect(self.start_scan)
        tools_menu.addAction("Analyze").triggered.connect(self.start_analysis)

    def _setup_toolbar(self):
        """Setup the main toolbar"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        
        # Add toolbar actions
        toolbar.addAction("New Project").triggered.connect(self.new_project)
        toolbar.addAction("Open Project").triggered.connect(self.open_project)
        toolbar.addSeparator()
        toolbar.addAction("Scan").triggered.connect(self.start_scan)
        toolbar.addAction("Analyze").triggered.connect(self.start_analysis)
        toolbar.addSeparator()
        toolbar.addAction("Refresh").triggered.connect(self.refresh_view)

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def refresh_view(self):
        """Refresh the current view"""
        for tab in self.tabs.values():
            if hasattr(tab, 'refresh'):
                tab.refresh()
        self.status_bar.showMessage("View refreshed")

    def new_project(self):
        """Create a new project"""
        self.status_bar.showMessage("Creating new project...")
        # Implementation would go here

    def open_project(self):
        """Open an existing project"""
        self.status_bar.showMessage("Opening project...")
        # Implementation would go here

    def start_scan(self):
        """Start a new scan"""
        self.status_bar.showMessage("Starting scan...")
        # Implementation would go here

    def start_analysis(self):
        """Start analysis of scan results"""
        self.status_bar.showMessage("Starting analysis...")
        # Implementation would go here
