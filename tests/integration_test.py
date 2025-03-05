import unittest
from src.main import BugHunterApp

class TestIntegration(unittest.TestCase):
    def test_app_initialization(self):
        app = BugHunterApp()
        self.assertIsNotNone(app)

if __name__ == '__main__':
    unittest.main()
