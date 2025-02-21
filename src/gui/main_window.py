"""
Enhanced MainWindow implementation for the BugHunter application.
Integrates all security tools, utilities, and services.
"""

import logging
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QLabel, QStatusBar, QToolBar, QMessageBox,
    QMenu, QMenuBar, QDockWidget, QSplitter,
    QTreeView, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSlot
from PyQt6.QtGui import QFont, QIcon, QAction, QKeySequence

# Core services
from services.config_manager import ConfigManager
from services.database import DatabaseManager
from services.user_auth import UserAuth
from services.tool_manager import ToolManager
from services.vulnerability_scanner import VulnerabilityScanner
from services.ai_system import AISystem
from services.collaboration_system import CollaborationSystem
from services.analytics_system import AnalyticsSystem

# Additional services
from services.notification import NotificationSystem
from services.chat_system import ChatSystem
from services.scope_manager import ScopeManager
from services.role_manager import RoleManager
from services.scanning_profiles import ScanningProfiles
from services.vulnerability_database import VulnerabilityDatabase
from services.wayback_machine_integration import WaybackMachineIntegration
from services.shodan_integration import ShodanIntegration

# Tabs
from tabs.ai_chat_tab import AIChatTab
from tabs.scanner_tab import ScannerTab
from tabs.nuclei_tab import NucleiTab
from tabs.amass_tab import AmassTab
from tabs.tool_manager_tab import ToolManagerTab
from tabs.bug_bounty_target_tab import BugBountyTargetTab
from tabs.collaboration_tab import CollaborationTab
from tabs.analytics_tab import AnalyticsTab
from tabs.settings_tab import SettingsTab
from tabs.wayback_tab import WaybackTab
from tabs.shodan_tab import ShodanTab
from tabs.scope_tab import ScopeTab
from tabs.role_tab import RoleTab
from tabs.profiles_tab import ProfilesTab
from tabs.vulnerability_db_tab import VulnerabilityDBTab

# Components
from components.status_window import StatusWindow
from components.notification_panel import NotificationPanel
from components.chat_panel import ChatPanel
from components.tool_panel import ToolPanel
from components.scope_tree import ScopeTree
from components.profile_manager import ProfileManager

class MainWindow(QMainWindow):
    """Enhanced main window of the BugHunter application"""
    
    def __init__(
        self,
        config_manager: ConfigManager,
        db_manager: DatabaseManager,
        auth_manager: UserAuth,
        tool_manager: ToolManager,
        vulnerability_scanner: VulnerabilityScanner,
        ai_system: AISystem,
        collaboration_system: CollaborationSystem,
        analytics_system: AnalyticsSystem,
        notification_system: NotificationSystem,
        chat_system: ChatSystem,
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
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.tool_manager = tool_manager
        self.vulnerability_scanner = vulnerability_scanner
        self.ai_system = ai_system
        self.collaboration_system = collaboration_system
        self.analytics_system = analytics_system
        self.notification_system = notification_system
        self.chat_system = chat_system
        self.scope_manager = scope_manager
        self.role_manager = role_manager
        self.scanning_profiles = scanning_profiles
        self.vulnerability_database = vulnerability_database
        self.wayback_integration = wayback_integration
        self.shodan_integration = shodan_integration
        
        # Initialize logger
        self.logger = logging.getLogger('BugHunter.MainWindow')
        
        # Setup authentication
        if not self._handle_authentication():
            raise Exception("Authentication failed")
        
        # Initialize UI components
        self._setup_window()
        self._setup_menubar()
        self._setup_toolbar()
        self._setup_statusbar()
        self._setup_dock_widgets()
        self._setup_central_widget()
        self._setup_tabs()
        self._setup_tray_icon()
        self._setup_shortcuts()
        self._setup_theme()
        
        # Initialize timers and background tasks
        self._setup_timers()
        
        # Connect signals
        self._connect_signals()
        
        self.logger.info("Main window initialized successfully")
