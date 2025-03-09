import unittest

from app.config import Config


class TestSanity(unittest.TestCase):
    def test_basic_config(self):
        config = Config()
        self.assert_equal(config.get("DB_HOST"), "localhost")

        if __name__ == "__main__":
            unittest.main()
