import unittest
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.services.config_manager import ConfigManager
from src.services.database import DatabaseManager
from src.services.user_auth import UserAuth

class TestUsability(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.main_window = MainWindow(
            config_manager=ConfigManager(),
            db_manager=DatabaseManager(),
            auth_manager=UserAuth(),
            tool_manager=None,
            vulnerability_scanner=None,
            ai_system=None,
            collaboration_system=None,
            analytics_system=None,
            notification_system=None,
            chat_system=None,
            scope_manager=None,
            role_manager=None,
            scanning_profiles=None,
            vulnerability_database=None,
            wayback_integration=None,
            shodan_integration=None
        )

    def test_main_window_title(self):
        self.assertEqual(self.main_window.windowTitle(), "BugHunter")

if __name__ == '__main__':
    unittest.main()
