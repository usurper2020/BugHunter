import unittest
from src.config import Config

class TestConfiguration(unittest.TestCase):
    def test_config_loading(self):
        config = Config()
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main()
