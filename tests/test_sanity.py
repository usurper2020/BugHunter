import unittest
from src.config import Config

class TestSanity(unittest.TestCase):
    def test_basic_config(self):
        config = Config()
        self.assertEqual(config.get('DB_HOST'), 'localhost')

if __name__ == '__main__':
    unittest.main()
