import unittest
from src.services.database import DatabaseManager

class TestBackupRecovery(unittest.TestCase):
    def test_backup_and_recovery(self):
        db_manager = DatabaseManager()
        backup = db_manager.backup()
        self.assertTrue(backup)
        recovery = db_manager.recover(backup)
        self.assertTrue(recovery)

if __name__ == '__main__':
    unittest.main()
