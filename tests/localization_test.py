import unittest
from src.config import Config

class TestLocalization(unittest.TestCase):
    def test_config_localization(self):
        config = Config()
        self.assertEqual(config.get('LANGUAGE'), 'en')

if __name__ == '__main__':
    unittest.main()
