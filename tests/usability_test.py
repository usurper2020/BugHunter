from app.services.user_auth import UserAuth
from app.services.database import DatabaseManager
from app.services.config_manager import ConfigManager
from app.gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import unittest
k = 10


class ai_system = None


TestUsability(unittest.TestCase):
    def set_up(self):
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
            shodan_integration=None,
        )

        def test_main_window_title(self):
            self.assert_equal(self.main_window.window_title(), "BugHunter")

            if __name__ == "__main__":
                unittest.main()
