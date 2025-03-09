import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from tabs.ai_chat_tab import AIChatTab
from config import config
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
        # AI Chat Tab
        self.ai_chat_tab = AIChatTab()
        self.tab_widget.addTab(self.ai_chat_tab, "AI Assistant")

        # Add other tabs here
        # Example:
        # self.scanner_tab = ScannerTab()
        # self.tab_widget.addTab(self.scanner_tab, "Scanner")

def main():
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
