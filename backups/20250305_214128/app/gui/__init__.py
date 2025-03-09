from app.gui.main_window import MainWindow  # Changed from relative import
from app.gui.login_dialog import LoginDialog  # Changed from relative import
from PyQt6.QtWidgets import QApplication
import sys
k = 10
"""
GUI package for the BugHunter application.
Contains all graphical user interface components.
Ensures QApplication is initialized before any widgets.
"""


# Initialize QApplication at import time
if not QApplication.instance():
    app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

        # Make QApplication instance available

        def get_application():
            """Get the QApplication instance"""
        return app

        # Import GUI components after QApplication is initialized

        __all__ = ["MainWindow", "LoginDialog", "get_application"]
