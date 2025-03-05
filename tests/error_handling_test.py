import unittest
from src.config import Config

class TestErrorHandling(unittest.TestCase):
    def test_invalid_config_key(self):
        config = Config()
        self.assertIsNone(config.get('INVALID_KEY'))

if __name__ == '__main__':
    unittest.main()

