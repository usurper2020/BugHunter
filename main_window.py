"""
Main window for the BugHunter application.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from tabs.ai_chat_tab import AIChatTab
from services.ai_system import AISystem
from config import config
from logger_config import logger_config

logger = logger_config.get_logger(__name__)

class MainWindow(QMainWindow):
    """Main window of the BugHunter application."""
    
    def __init__(self):
        """Initialize the main window instance."""
        super().__init__()
        
        # Initialize core systems
        self.ai_system = AISystem()
        self.ai_system.initialize()  # Important: Initialize the AI system
        
        self.init_ui()

    def init_ui(self):
        """Initialize and configure the user interface."""
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
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background: #1e1e1e;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #2196f3;
            }
            QTabBar::tab:hover:!selected {
                background: #1976d2;
            }
        """)

    def setup_tabs(self):
        """Set up and configure application tabs."""
        try:
            # AI Chat Tab with initialized AI system
            self.ai_chat_tab = AIChatTab(ai_system=self.ai_system)
            self.tab_widget.addTab(self.ai_chat_tab, "AI Assistant")
            
            logger.info("AI Chat tab initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)
            raise

def main():
    """Entry point for the BugHunter application."""
    try:
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
