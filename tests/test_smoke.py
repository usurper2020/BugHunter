import unittest
from src.main import BugHunterApp

class TestSmoke(unittest.TestCase):
    def test_app_startup(self):
        app = BugHunterApp()
        self.assertIsNotNone(app)

if __name__ == '__main__':
    unittest.main()

