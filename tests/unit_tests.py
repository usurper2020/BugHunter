import unittest
from src.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_get_database_url(self):
        expected_url = "postgresql://bughunter:@localhost:5432/bughunter"
        self.assertEqual(self.config.get_database_url(), expected_url)

    def test_get_redis_url(self):
        expected_url = "redis://localhost:6379/0"
        self.assertEqual(self.config.get_redis_url(), expected_url)

if __name__ == '__main__':
    unittest.main()
