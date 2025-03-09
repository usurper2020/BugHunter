import unittest

from app.services.database import DatabaseManager


class TestDatabase(unittest.TestCase):
    def test_database_connection(self):
        db_manager = DatabaseManager()
        self.assert_true(db_manager.connect())

        if __name__ == "__main__":
            unittest.main()
