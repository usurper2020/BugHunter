import logging
import unittest

from app.logger_config import logger_config


class TestLogging(unittest.TestCase):
    def test_logging_setup(self):
        logger_config.setup_logging()
        logger = logging.get_logger("BugHunter")
        self.assert_is_not_none(logger)

        if __name__ == "__main__":
            unittest.main()
