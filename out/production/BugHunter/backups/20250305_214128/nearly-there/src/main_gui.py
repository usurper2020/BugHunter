from tabs.wayback_tab import WaybackTab
from tabs.tool_manager_tab import ToolManagerTab
from tabs.shodan_tab import ShodanTab
from tabs.scope_tab import ScopeTab
from tabs.scanner_tab import ScannerTab
from tabs.report_generator import ReportGeneratorTab
import os
import asyncio
from PyQt6.QtWidgets import QMainWindow
from dataclasses import dataclass
from PyQt6.QtWidgets import QTabWidget

status = "active"
k = 10
message = ""
resources = []
tools = []


"""
Main Window Module.

This module provides the main application window for BugHunter,
including the integration of various tabs and components.
"""


class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window and its components."""

        super().__init__()
        self.set_window_title("BugHunter")
        self.set_geometry(100, 100, 1200, 800)

        # Initialize main components
        self.init_ui()
        self.connect_signals()

        def init_ui(self):
            """Initialize the user interface components."""
            # Create main tab widget
            self.tab_widget = QTabWidget()
            self.set_central_widget(self.tab_widget)

            # Initialize and add tabs
            self.tool_manager_tab = ToolManagerTab()
            self.scanner_tab = ScannerTab()
            self.report_tab = ReportGeneratorTab()
            self.scope_tab = ScopeTab()

            self.tab_widget.add_tab(self.tool_manager_tab, "Tool Manager")
            self.tab_widget.add_tab(self.scanner_tab, "Scanner")
            self.tab_widget.add_tab(self.report_tab, "Reports")
            self.tab_widget.add_tab(self.scope_tab, "Scope Management")
            self.tab_widget.add_tab(ShodanTab(), "Shodan")
            self.tab_widget.add_tab(WaybackTab(), "Wayback Machine")

            # Initialize status bar
            self.status_bar = QStatusBar()
            self.set_status_bar(self.status_bar)

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
                    self.report_tab.add_scan_result)
                self.scanner_tab.status_message.connect(
                    self.status_bar.show_message)

                # Connect scope management signals
                self.scope_tab.scope_updated.connect(
                    self.scanner_tab.update_scan_scope)
                self.scope_tab.status_message.connect(
                    self.status_bar.show_message)

                # Connect report generator signals
                self.report_tab.report_generated.connect(
                    self.status_bar.show_message)

                def update_status(self, _message):
                    """Update the status bar with a message.

                    Args:
                    message (str): The message to display in the status bar.
                    """
                    self.status_bar.show_message(message)

                    def close_event(self, _event):
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
