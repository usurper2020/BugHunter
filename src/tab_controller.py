from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from tabs.ai_chat_tab import AIChatTab
from src.scanner_tab import ScannerTab
from src.core import logger_config

logger = logger_config.get_logger(__name__)

class TabController:
    """Controls and manages application tabs"""
    
    @staticmethod
    def setup_tabs(tab_widget: QTabWidget):
        """Set up all application tabs"""
        try:
            # AI Chat Tab
            ai_chat_tab = AIChatTab()
            tab_widget.addTab(ai_chat_tab, "AI Assistant")
            logger.info("AI Assistant tab added successfully")

            # Scanner Tab
            scanner_tab = ScannerTab()
            tab_widget.addTab(scanner_tab, "Vulnerability Scanner")
            logger.info("Scanner tab added successfully")

            # Reports Tab
            reports_tab = QWidget()
            reports_layout = QVBoxLayout(reports_tab)
            tab_widget.addTab(reports_tab, "Reports")
            logger.info("Reports tab added successfully")

            # Analytics Tab
            analytics_tab = QWidget()
            analytics_layout = QVBoxLayout(analytics_tab)
            tab_widget.addTab(analytics_tab, "Analytics")
            logger.info("Analytics tab added successfully")

            # Settings Tab
            settings_tab = QWidget()
            settings_layout = QVBoxLayout(settings_tab)
            tab_widget.addTab(settings_tab, "Settings")
            logger.info("Settings tab added successfully")

            # Collaboration Tab
            collab_tab = QWidget()
            collab_layout = QVBoxLayout(collab_tab)
            tab_widget.addTab(collab_tab, "Collaboration")
            logger.info("Collaboration tab added successfully")

        except Exception as e:
            logger.error(f"Error setting up tabs: {str(e)}", exc_info=True)
            raise
