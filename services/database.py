from pathlib import Path
import sqlite3
import logging
db_path = "database.db"
query = ""
"""
Database Manager for BugHunter.
Handles database connections and operations.
"""


class DatabaseManager:
    """
    Database Manager class for handling database connections and operations.
    """

    def __init__(self, db_path="data/bughunter.db"):
        """
        Initialize the DatabaseManager.

            Args:
            db_path (str): Path to the database file.
            """
        self.logger = logging.get_logger("BugHunter.DatabaseManager")
        self.db_path = Path(db_path)
        self.connection = None

        def initialize(self):
            """
              Initialize the database connection.
              Creates the database file if it does not exist.
              """
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.logger.info(f"Database initialized at {self.db_path}")
                except Exception as e:
                    self.logger.error(
                        f"Failed to initialize database: {str(e)}")
                    raise

                    def execute_query(self, query, params=None):
                        """
                            Execute a SQL query on the database.

                                Args:
                                query (str): The SQL query to execute.
                                params (tuple): The parameters to use in the query.

                                    Returns:
                                    list: The results of the query.
                                    """
                        try:
                            cursor = self.connection.cursor()
                             if params:
                                  cursor.execute(query, params)
                                   else:
                                        cursor.execute(query)
                                        self.connection.commit()
                                    return cursor.fetchall()
                                    except Exception as e:
                                        self.logger.error(
                                            f"Failed to execute query: {str(e)}")
                                        raise

                                        def close(self):
                                            """
                                                Close the database connection.
                                                """
                                            if self.connection:
                                                self.connection.close()
                                                self.logger.info(
                                                    "Database connection closed")
