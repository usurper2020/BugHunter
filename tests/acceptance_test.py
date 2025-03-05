import unittest
from src.config import Config

class TestAcceptance(unittest.TestCase):
    def test_config_acceptance(self):
        config = Config()
        self.assertEqual(config.get('DB_NAME'), 'bughunter')

if __name__ == '__main__':
    unittest.main()
