"""
Main Window Module.

This module provides the main application window for BugHunter,
including the integration of various tabs and components.

Classes:
    MainWindow: Main application window class.
"""

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar
from tabs.tool_manager_tab import ToolManagerTab
from tabs.scanner_tab import ScannerTab
from tabs.report_generator import ReportGeneratorTab
from tabs.shodan_tab import ShodanTab
from tabs.wayback_tab import WaybackTab
from tabs.scope_tab import ScopeTab


# main_gui.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
import sys
import asyncio
import qasync
from ai_tab import AITab
from ai_system import AISystem, SecureConfigManager, AIClientFactory
import redis
import aiohttp
import os
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self, ai_system):
        super().__init__()
        self.ai_system = ai_system
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI System GUI")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.ai_tab = AITab(self.ai_system)
        self.tabs.addTab(self.ai_tab, "AI Interaction")

async def main():
    encryption_key = os.getenv('ENCRYPTION_KEY')
    config_manager = SecureConfigManager(Path('src/config/ai_config.json'), encryption_key)
    config = config_manager.get('ai_config')
    cache_client = redis.Redis(host='localhost', port=6379, db=0)
    async with aiohttp.ClientSession() as session:
        ai_client = await AIClientFactory.create_client(config['ai_api_type'], config, session)
        ai_system = AISystem(config_manager, ai_client, cache_client)

        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)

        main_window = MainWindow(ai_system)
        main_window.show()

        with loop:
            loop.run_forever()


class MainWindow(QMainWindow):
    """
    Main application window for BugHunter.

    Attributes:
        tab_widget (QTabWidget): Main tab widget for the application.
        tool_manager_tab (ToolManagerTab): Tool management tab instance.
        scanner_tab (ScannerTab): Scanner tab instance.
        report_tab (ReportGeneratorTab): Report generator tab instance.
        scope_tab (ScopeTab): Scope management tab instance.
        status_bar (QStatusBar): Status bar for system messages.
    ""

    def __init__(self):
        """Initialize the main window and its components."""
        super().__init__()
        self.setWindowTitle("BugHunter")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize main components
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Initialize the user interface components."""
        # Create main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Initialize and add tabs
        self.tool_manager_tab = ToolManagerTab()
        self.scanner_tab = ScannerTab()
        self.report_tab = ReportGeneratorTab()
        self.scope_tab = ScopeTab()

        self.tab_widget.addTab(self.tool_manager_tab, "Tool Manager")
        self.tab_widget.addTab(self.scanner_tab, "Scanner")
        self.tab_widget.addTab(self.report_tab, "Reports")
        self.tab_widget.addTab(self.scope_tab, "Scope Management")
        self.tab_widget.addTab(ShodanTab(), "Shodan")
        self.tab_widget.addTab(WaybackTab(), "Wayback Machine")

        # Initialize status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def connect_signals(self):
        """Connect signals between components."""
        # Connect tool manager signals
        self.tool_manager_tab.tool_installed.connect(
            self.scanner_tab.update_tools_list
        )
        self.tool_manager_tab.tool_removed.connect(
            self.scanner_tab.update_tools_list
        )
        
        # Connect scanner signals
        self.scanner_tab.scan_complete.connect(
            self.report_tab.add_scan_result
        )
        self.scanner_tab.status_message.connect(
            self.status_bar.showMessage
        )
        
        # Connect scope management signals
        self.scope_tab.scope_updated.connect(
            self.scanner_tab.update_scan_scope
        )
        self.scope_tab.status_message.connect(
            self.status_bar.showMessage
        )
        
        # Connect report generator signals
        self.report_tab.report_generated.connect(
            self.status_bar.showMessage
        )

    def update_status(self, message):
        """Update the status bar with a message.
        
        Args:
            message (str): The message to display in the status bar.
        """
        self.status_bar.showMessage(message)

    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event (QCloseEvent): The close event.
        """
        # Clean up resources before closing
        self.tool_manager_tab.cleanup()
        self.scanner_tab.cleanup()
        self.report_tab.cleanup()
        self.scope_tab.cleanup()
        event.accept()

if __name__ == "__main__":
    asyncio.run(main())