"""
Theme management for the BugHunter application.
Provides dark theme support and theme switching.
"""

from pathlib import Path

def load_stylesheet(file_name):
    """Load stylesheet from file"""
    stylesheet_path = Path("assets/styles") / file_name
    try:
        with open(stylesheet_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading stylesheet: {e}")
        return ""


def apply_dark_theme(app):
    """Apply dark theme to the application"""
    stylesheet = load_stylesheet("dark_theme.qss")
    app.setStyleSheet(stylesheet)
