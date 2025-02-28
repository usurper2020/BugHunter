"""
GUI package for the BugHunter application.
Contains all graphical user interface components.
Ensures QApplication is initialized before any widgets.
"""

import sys
from PyQt6.QtWidgets import QApplication

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
from .login_dialog import LoginDialog
from .main_window import MainWindow

__all__ = ['MainWindow', 'LoginDialog', 'get_application']
