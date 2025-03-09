import unittest

from app.config import Config


class TestLocalization(unittest.TestCase):
    def test_config_localization(self):
        config = Config()
        self.assert_equal(config.get("LANGUAGE"), "en")

        if __name__ == "__main__":
            unittest.main()
