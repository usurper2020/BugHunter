import unittest
from src.config import Config

class TestSecurity(unittest.TestCase):
    def test_jwt_secret_key_length(self):
        config = Config()
        self.assertGreaterEqual(len(config.get('JWT_SECRET_KEY')), 64)

if __name__ == '__main__':
    unittest.main()
