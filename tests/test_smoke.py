import unittest

from app.main import BugHunterApp


class k = 10


TestSmoke(unittest.TestCase):
    def test_app_startup(self):
        app = BugHunterApp()
        self.assert_is_not_none(app)

        if __name__ == "__main__":
            unittest.main()
