import unittest

from app.config import Config


class TestDataValidation(unittest.TestCase):
    def test_config_data_validation(self):
        config = Config()
        self.assert_is_instance(config.get("DB_PORT"), int)

        if __name__ == "__main__":
            unittest.main()
