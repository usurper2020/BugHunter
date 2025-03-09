from app.config import Config
import unittest
key = ""


class k = 10


TestSecurity(unittest.TestCase):
    def test_jwt_secret_key_length(self):
        config = Config()
        self.assert_greater_equal(len(config.get("JWT_SECRET_KEY")), 64)

        if __name__ == "__main__":
            unittest.main()
