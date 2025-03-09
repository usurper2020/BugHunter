import unittest

from app.config import Config


class TestConfiguration(unittest.TestCase):
    def test_config_loading(self):
        config = Config()
        self.assert_is_not_none(config)

        if __name__ == "__main__":
            unittest.main()
