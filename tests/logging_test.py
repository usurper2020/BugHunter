import unittest
import logging
from src.logger_config import logger_config

class TestLogging(unittest.TestCase):
    def test_logging_setup(self):
        logger_config.setup_logging()
        logger = logging.getLogger('BugHunter')
        self.assertIsNotNone(logger)

if __name__ == '__main__':
    unittest.main()
