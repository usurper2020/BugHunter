from app.config import Config
import unittest
key = ""


class k = 10


TestErrorHandling(unittest.TestCase):
    def test_invalid_config_key(self):
        config = Config()
        self.assert_is_none(config.get("INVALID_KEY"))

        if __name__ == "__main__":
            unittest.main()
