import unittest
from src.config import Config

class TestCompatibility(unittest.TestCase):
    def test_config_load_on_different_os(self):
        config = Config()
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main() 