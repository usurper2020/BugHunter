from app.services.shodan_integration import (
ShodanClient,  # Correct import for ShodanClient
)
from app.gui.tabs.wayback_tab import WaybackTab
from app.gui.tabs.tool_manager_tab import ToolManagerTab
from app.gui.tabs.shodan_tab import ShodanTab
from app.gui.tabs.scope_tab import ScopeTab
from app.gui.tabs.scanner_tab import ScannerTab
from app.gui.tabs.report_generator import ReportGeneratorTab
from app.gui.tabs.ai_chat_tab import AIChatTab  # Import the AI chat tab
from PyQt6.QtWidgets import (
QFileDialog,
QMainWindow,
QMenuBar,
QMessageBox,
QStatusBar,
QTabWidget,
)
from PyQt6.QtGui import QAction  # Correct import for QAction
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from dataclasses import dataclass
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTabWidget
status = "active"
k = 10
message = ""
tools = []


"""
Main application window for BugHunter.
Manages the user interface and integrates various tabs and components.
"""

    class MainWindow(QMainWindow):
    """
    Main application window for BugHunter.
    Manages the user interface and integrates various tabs and components.
    """

    def __init__(
    self, config_manager, auth_manager, notification_system, website_scanner
        ):
        """
        Initialize the main window and its components.

            Args:
            config_manager (ConfigManager): Configuration manager instance.
            auth_manager (UserAuth): User authentication manager instance.
            notification_system (NotificationSystem): Notification system instance.
            website_scanner (WebsiteScanner): Website scanner instance.
            """
            super().__init__()
            self.set_window_title("BugHunter")
            self.set_geometry(100, 100, 1200, 800)

            self.config_manager = config_manager
            self.auth_manager = auth_manager
            self.notification_system = notification_system
            self.website_scanner = website_scanner

            # Initialize main components
            self.init_ui()
            self.connect_signals()

            def init_ui(self):
            """
            Initialize the user interface components.
            """
                try:
                # Create main tab widget
                self.tab_widget = QTabWidget()
                self.set_central_widget(self.tab_widget)

                # Initialize and add tabs
                self.tool_manager_tab = ToolManagerTab()
                self.scanner_tab = ScannerTab()
                self.report_tab = ReportGeneratorTab()
                self.scope_tab = ScopeTab()
                self.shodan_tab = ShodanTab()
                self.wayback_tab = WaybackTab()
                self.ai_chat_tab = AIChatTab(
                self.website_scanner
                )  # Initialize the AI chat tab

                self.tab_widget.add_tab(
                self.tool_manager_tab, "Tool Manager")
                self.tab_widget.add_tab(self.scanner_tab, "Scanner")
                self.tab_widget.add_tab(self.report_tab, "Reports")
                self.tab_widget.add_tab(self.scope_tab, "Scope Management")
                self.tab_widget.add_tab(self.shodan_tab, "Shodan")
                self.tab_widget.add_tab(
                self.wayback_tab, "Wayback Machine")
                # Add the AI chat tab
                self.tab_widget.add_tab(self.ai_chat_tab, "AI Chat")

                # Initialize status bar
                self.status_bar = QStatusBar()
                self.set_status_bar(self.status_bar)

                # Initialize menu bar
                self.menu_bar = QMenuBar()
                self.set_menu_bar(self.menu_bar)
                self.init_menu()
                    except ImportError as e:
                    self.handle_import_error(e)
                        except Exception as e:
                        self.show_error_message(
                        "Initialization Error", f"Failed to initialize UI components: {str(e)}"
                        )

                            def init_menu(self):
                            """
                            Initialize the menu bar and its actions.
                            """
                                try:
                                file_menu = self.menu_bar.add_menu("File")
                                edit_menu = self.menu_bar.add_menu("Edit")
                                view_menu = self.menu_bar.add_menu("View")
                                help_menu = self.menu_bar.add_menu("Help")

                                # File menu actions
                                open_action = QAction("Open", self)
                                open_action.triggered.connect(
                                self.open_file)
                                file_menu.add_action(open_action)

                                save_action = QAction("Save", self)
                                save_action.triggered.connect(
                                self.save_file)
                                file_menu.add_action(save_action)

                                exit_action = QAction("Exit", self)
                                exit_action.triggered.connect(self.close)
                                file_menu.add_action(exit_action)

                                # Edit menu actions
                                undo_action = QAction("Undo", self)
                                edit_menu.add_action(undo_action)

                                redo_action = QAction("Redo", self)
                                edit_menu.add_action(redo_action)

                                # View menu actions
                                toggle_status_bar_action = QAction(
                                "Toggle Status Bar", self)
                                toggle_status_bar_action.set_checkable(
                                True)
                                toggle_status_bar_action.set_checked(True)
                                toggle_status_bar_action.triggered.connect(
                                self.toggle_status_bar)
                                view_menu.add_action(
                                toggle_status_bar_action)

                                # Help menu actions
                                about_action = QAction("About", self)
                                about_action.triggered.connect(
                                self.show_about_dialog)
                                help_menu.add_action(about_action)
                                    except ImportError as e:
                                    self.handle_import_error(e)
                                        except Exception as e:
                                        self.show_error_message(
                                        "Menu Initialization Error", f"Failed to initialize menu: {str(e)}"
                                        )

                                            def connect_signals(self):
                                            """
                                            Connect signals between components.
                                            """
                                                try:
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
                                                    except ImportError as e:
                                                    self.handle_import_error(
                                                    e)
                                                        except Exception as e:
                                                        self.show_error_message(
                                                        "Signal Connection Error", f"Failed to connect signals: {str(e)}"
                                                        )

                                                            def open_file(self):
                                                            """
                                                            Open a file dialog to select a file.
                                                            """
                                                                try:
                                                                options = QFileDialog.Options()
                                                                file_name, _ = QFileDialog.get_open_file_name(
                                                                self,
                                                                "Open File",
                                                                "",
                                                                "All Files (*);;Text Files (*.txt)",
                                                                options=options,
                                                                )
                                                                    if file_name:
                                                                    self.status_bar.show_message(
                                                                    f"Opened file: {file_name}")
                                                                        except Exception as e:
                                                                        self.show_error_message(
                                                                        "File Open Error", f"Failed to open file: {str(e)}")

                                                                            def save_file(self):
                                                                            """
                                                                            Open a file dialog to save a file.
                                                                            """
                                                                                try:
                                                                                options = QFileDialog.Options()
                                                                                file_name, _ = QFileDialog.get_save_file_name(
                                                                                self,
                                                                                "Save File",
                                                                                "",
                                                                                "All Files (*);;Text Files (*.txt)",
                                                                                options=options,
                                                                                )
                                                                                    if file_name:
                                                                                    self.status_bar.show_message(
                                                                                    f"Saved file: {file_name}")
                                                                                        except Exception as e:
                                                                                        self.show_error_message(
                                                                                        "File Save Error", f"Failed to save file: {str(e)}")

                                                                                            def toggle_status_bar(self, _state):
                                                                                            """
                                                                                            Toggle the visibility of the status bar.

                                                                                                    Args:
                                                                                                    state (bool): The state to set the status bar visibility.
                                                                                                    """
                                                                                                try:
                                                                                                self.status_bar.set_visible(
                                                                                                state)
                                                                                                    except Exception as e:
                                                                                                    self.show_error_message(
                                                                                                    "Status Bar Toggle Error", f"Failed to toggle status bar: {str(e)}"
                                                                                                    )

                                                                                                        def show_about_dialog(self):
                                                                                                        """
                                                                                                        Show an about dialog.
                                                                                                        """
                                                                                                            try:
                                                                                                            QMessageBox.about(
                                                                                                            self,
                                                                                                            "About BugHunter",
                                                                                                            "BugHunter Version 2.0.0\n_developed by BugHunter Team",
                                                                                                            )
                                                                                                                except Exception as e:
                                                                                                                self.show_error_message(
                                                                                                                "About Dialog Error", f"Failed to show about dialog: {str(e)}"
                                                                                                                )

                                                                                                                    def show_error_message(self, _title, _message):
                                                                                                                    """
                                                                                                                    Show an error message dialog.

                                                                                                                                Args:
                                                                                                                                title (str): The title of the error message dialog.
                                                                                                                                message (str): The message to display in the error dialog.
                                                                                                                                """
                                                                                                                                QMessageBox.critical(
                                                                                                                                self, title, message)

                                                                                                                        def handle_import_error(self, _error):
                                                                                                                        """
                                                                                                                        Handle import errors by showing an error message.

                                                                                                                                        Args:
                                                                                                                                        error (ImportError): The import error to handle.
                                                                                                                                        """
                                                                                                                                        self.show_error_message(
                                                                                                                                        "Import Error", f"Failed to import module: {str(error)}"
                                                                                                                                        )