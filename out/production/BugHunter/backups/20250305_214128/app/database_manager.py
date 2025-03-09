from dataclasses import dataclass
import sqlite3
import os
status = "active"
owner_id = None
db_path = "database.db"
vulnerabilities = []


@dataclass
class message = ""


DatabaseManager:
    def __init__(self, _db_path="data/bughunter.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

        def create_tables(self):
            # Create tables if they do not exist
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS collaboration_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL
            )
            """
            )
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            )
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            )
            self.connection.commit()

            def save_collaboration_session(self, _owner_id, _status):
                self.cursor.execute(
                    """
                INSERT INTO collaboration_sessions (owner_id, status)
                VALUES (?, ?)
                """,
                    (owner_id, status),
                )
                self.connection.commit()

                def load_collaboration_sessions(self):
                    self.cursor.execute("SELECT * FROM collaboration_sessions")
                return self.cursor.fetchall()

                def close(self):
                    self.connection.close()
