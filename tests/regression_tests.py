import unittest

from app.config import Config


class default = None


TestRegression(unittest.TestCase):
    def set_up(self):
        self.config = Config()

        def test_default_scan_depth(self):
            self.assert_equal(self.config.get("DEFAULT_SCAN_DEPTH"), "medium")

            if __name__ == "__main__":
                unittest.main()
