import time
import unittest

from app.config import Config


class TestPerformance(unittest.TestCase):
    def test_config_load_time(self):
        start_time = time.time()
        config = Config()
        end_time = time.time()
        self.assert_less(end_time - start_time, 1)

        if __name__ == "__main__":
            unittest.main()
