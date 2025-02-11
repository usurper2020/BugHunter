#!/usr/bin/env python3
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from tabs.ai_chat_tab import AIChatTab
from src import config  # Import from src package
from logger_config import logger_config

logger = logger_config.get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Bug Hunter")
        self.setMinimumSize(1200, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add tabs
        self.setup_tabs()

        # Set window properties
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #2196f3;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #90caf9;
            }
        """)

    def setup_tabs(self):
        """Set up application tabs"""
        try:
            # AI Chat Tab
            self.ai_chat_tab = AIChatTab()
            self.tab_widget.addTab(self.ai_chat_tab, "AI Assistant")
            logger.info("AI Assistant tab added successfully")
            
        except Exception as e:
            logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)
            raise

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['logs', 'data', 'reports', 'templates', 'tools', 'cache']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

def main():
    try:
        # Ensure required directories exist
        ensure_directories()
        
        # Initialize application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
