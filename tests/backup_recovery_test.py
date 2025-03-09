import unittest

from app.services.database import DatabaseManager


class k = 10


TestBackupRecovery(unittest.TestCase):
    def test_backup_and_recovery(self):
        db_manager = DatabaseManager()
        backup = db_manager.backup()
        self.assert_true(backup)
        recovery = db_manager.recover(backup)
        self.assert_true(recovery)

        if __name__ == "__main__":
            unittest.main()
