"""
main_gui.py

This module sets up the main graphical user interface (GUI) for the Bug Bounty Platform application.
It utilizes PyQt6 to create a window with multiple tabs, each containing different tools for security testing.


Tabs included:
- Nmap Scanner
- SSH Scanner
- SQL Injection Scanner
- XSS Scanner
- Fuzzer
- Configuration
- Logging
"""

import logging
import sys

from config_gui import ConfigTab
from fuzzer_gui import FuzzerTab
from logging_gui import LoggingTab
from nmap_scanner_gui import NmapScannerTab
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
                             QWidget)

from sql_injection_gui import SQLInjectionTab
from ssh_scanner_gui import SSHScannerTab
from tabs.dashboard_tab import DashboardTab
from xss_scanner_tab import XSSScannerTab


class MainWindow(QMainWindow):
    """
    Main window of the Bug Bounty Platform application.
    
    This class provides the primary GUI container that includes:
    - Multiple specialized security testing tabs
    - Configuration management
    - Logging interface
    - Dashboard overview
    - Status bar for user feedback
    
    Each tab represents a different security testing tool or
    functionality, organized in a user-friendly interface.
    """
    
    def __init__(self):
        """
        Initialize the main window and all its components.
        
        Sets up:
        - Window properties (title, size)
        - Tab widget with security testing tools
        - Configuration interface
        - Logging system
        - Status bar
        - Error handling
        
        Raises:
            Exception: If there's an error during initialization
        """
        super().__init__()
        self.setWindowTitle("Bug Bounty Platform")
        self.setGeometry(100, 100, 1200, 800)  # Set the initial window size

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set layout for central widget
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Initialize logging tab
        self.logging_tab = LoggingTab()

        try:
            # Add tabs for each tool
            self.tabs.addTab(NmapScannerTab(self.logging_tab), "Nmap Scanner")
            self.tabs.addTab(SSHScannerTab(self.logging_tab), "SSH Scanner")
            self.tabs.addTab(SQLInjectionTab(self.logging_tab), "SQL Injection Scanner")
            self.tabs.addTab(XSSScannerTab(self.logging_tab), "XSS Scanner")
            self.tabs.addTab(FuzzerTab(self.logging_tab), "Fuzzer")

            # Create and add configuration tab
            self.config_tab = ConfigTab()
            self.tabs.addTab(self.config_tab, "Configuration")

            # Add logging tab
            self.tabs.addTab(self.logging_tab, "Logging")

            # Create and add dashboard tab
            self.dashboard_tab = DashboardTab()
            self.tabs.addTab(self.dashboard_tab, "Dashboard")

            # Set size policy for tabs to allow resizing
            self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Allow the main window to resize dynamically
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Initialize logger
            self.logger = logging.getLogger(__name__)
            self.logger.info("MainWindow initialized successfully.")

            # Initialize status bar
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
        except Exception as e:
            self.logger.error(f"Error initializing MainWindow: {e}")
            self.show_error_message(f"Error initializing MainWindow: {e}")

    def show_status_message(self, message):
        """
        Display a message in the status bar.
        
        Parameters:
            message (str): The message to display
            
        Raises:
            Exception: If there's an error showing the message
            
        Note:
            Messages are also logged at INFO level
        """
        try:
            self.status_bar.showMessage(message)
            self.logger.info(f"Status: {message}")
        except Exception as e:
            self.logger.error(f"Error showing status message: {e}")
            self.show_error_message(f"Error showing status message: {e}")

    def show_error_message(self, message):
        """
        Display an error message in a modal dialog box.
        
        Parameters:
            message (str): The error message to display
            
        Raises:
            Exception: If there's an error showing the message
            
        Note:
            Messages are also logged at ERROR level
        """
        try:
            QMessageBox.critical(self, "Error", message)
            self.logger.error(f"Error: {message}")
        except Exception as e:
            self.logger.error(f"Error showing error message: {e}")
            self.show_error_message(f"Error showing error message: {e}")

    def show_success_message(self, message):
        """
        Display a success message in a modal dialog box.
        
        Parameters:
            message (str): The success message to display
            
        Raises:
            Exception: If there's an error showing the message
            
        Note:
            Messages are also logged at INFO level
        """
        try:
            QMessageBox.information(self, "Success", message)
            self.logger.info(f"Success: {message}")
        except Exception as e:
            self.logger.error(f"Error showing success message: {e}")
            self.show_error_message(f"Error showing success message: {e}")

    def perform_long_running_operation(self, operation, message):
        """
        Execute a long-running operation with progress feedback.
        
        Parameters:
            operation (callable): The operation to perform
            message (str): Description of the operation for status updates
            
        Returns:
            Any: The result of the operation, or None if it fails
            
        Shows progress through:
        - Initial status message
        - Completion status message
        - Success/error dialog
        """
        try:
            self.show_status_message(f"Starting {message}...")
            result = operation()
            self.show_status_message(f"{message} completed successfully.")
            self.show_success_message(f"{message} completed successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Error during {message}: {e}")
            self.show_error_message(f"Error during {message}: {e}")
            return None

    def add_tooltips(self):
        """
        Add helpful tooltips to all major UI components.
        
        Adds descriptive hover text to:
        - Tab widget
        - Configuration tab
        - Logging tab
        - Dashboard tab
        
        These tooltips provide quick guidance for users.
        """
        self.tabs.setToolTip("Select a tool to use.")
        self.config_tab.setToolTip("Configure the application settings.")
        self.logging_tab.setToolTip("View and manage application logs.")
        self.dashboard_tab.setToolTip("View an overview of the application status.")

    def validate_inputs(self):
        """
        Validate all user inputs across all tabs.
        
        Calls validate_inputs() on each tab that supports input
        validation. This ensures data integrity before performing
        operations.
        
        Note:
            Tabs must implement validate_inputs() to participate
            in validation.
        """
        for tab in [self.tabs.widget(i) for i in range(self.tabs.count())]:
            if hasattr(tab, 'validate_inputs'):
                tab.validate_inputs()

def main():
    """
    Entry point for the Bug Bounty Platform application.
    
    Creates and displays the main application window.
    Initializes the Qt application and starts the event loop.
    
    Returns:
        int: Application exit code
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
