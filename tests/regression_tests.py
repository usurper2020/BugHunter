import unittest
from src.config import Config

class TestRegression(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_default_scan_depth(self):
        self.assertEqual(self.config.get('DEFAULT_SCAN_DEPTH'), 'medium')

if __name__ == '__main__':
    unittest.main()
