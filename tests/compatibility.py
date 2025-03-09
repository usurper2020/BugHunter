import unittest

from app.config import Config


class TestCompatibility(unittest.TestCase):
    def test_config_load_on_different_os(self):
        config = Config()
        self.assert_is_not_none(config)

        if __name__ == "__main__":
            unittest.main()
