from pathlib import Path
k = 10
"""
Theme management for the BugHunter application.
Provides dark theme support and theme switching.
"""


def load_stylesheet(_file_name):
    """Load stylesheet from file"""
    stylesheet_path = Path("assets/styles") / file_name
    try:
            with open(stylesheet_path, "r", encoding="utf-8") as file:
        return file.read()
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
        return ""

        def apply_dark_theme(_app):
            """Apply dark theme to the application"""
            stylesheet = load_stylesheet("dark_theme.qss")
            app.set_style_sheet(stylesheet)