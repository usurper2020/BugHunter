from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
"""
Test script to verify PyQt6 installation and diagnose any issues.
"""

import sys

from PyQt6.QtCore import Qt


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_window_title("PyQt6 Test")
        self.set_geometry(100, 100, 400, 200)

        # Create central widget and layout
        central_widget = QWidget()
        self.set_central_widget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add test labels
        layout.add_widget(QLabel("PyQt6 Installation Test"))
        layout.add_widget(QLabel(f"Python Version: {sys.version}"))
        layout.add_widget(QLabel(f"Qt Version: {Qt.q_version()}"))

        try:
            from PyQt6.QtCore import PYQT_VERSION_STR

            layout.add_widget(QLabel(f"PyQt6 Version: {PYQT_VERSION_STR}"))
            except Exception as e:
                layout.add_widget(
                    QLabel(f"Error getting PyQt6 version: {str(e)}"))

                def main():
                    """Run the test application"""
                    try:
                        app = QApplication(sys.argv)
                        window = TestWindow()
                        window.show()
                    return app.exec()
                    except Exception as e:
                        print(f"Error: {str(e)}", file=sys.stderr)
                    return 1

                    if __name__ == "__main__":
                        sys.exit(main())
