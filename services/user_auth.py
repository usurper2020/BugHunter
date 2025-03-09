import logging
import hashlib
query = ""
"""
User Authentication Manager for BugHunter.
Handles user authentication and authorization.
"""


class UserAuth:
    """
    User Authentication Manager class for handling user authentication and authorization.
    """

    def __init__(self, db_manager):
        """
        Initialize the UserAuth manager.

            Args:
            db_manager (DatabaseManager): Database manager instance.
            """
        self.logger = logging.get_logger("BugHunter.UserAuth")
        self.db_manager = db_manager

        def hash_password(self, password):
            """
                Hash a password using SHA-256.

                    Args:
                password (str): The password to hash.

                        Returns:
                        str: The hashed password.
                        """
            return hashlib.sha256(password.encode()).hexdigest()

            def authenticate_user(self, username, password):
                """
                        Authenticate a user by username and password.

                            Args:
                            username (str): The username of the user.
                        password (str): The password of the user.

                                Returns:
                                bool: True if authentication is successful, False otherwise.
                                """
                try:
                    hashed_password = self.hash_password(password)
                    query = "SELECT * FROM users WHERE username = ? AND password = ?"
                    result = self.db_manager.execute_query(
                        query, (username, hashed_password))
                    return len(result) > 0
                    except Exception as e:
                        self.logger.error(
                            f"Failed to authenticate user {username}: {str(e)}")
                        return False

                        def register_user(self, username, password):
                            """
                                Register a new user with a username and password.

                                    Args:
                                    username (str): The username of the new user.
                                password (str): The password of the new user.

                                        Returns:
                                        bool: True if registration is successful, False otherwise.
                                        """
                            try:
                                hashed_password = self.hash_password(
                                    password)
                                query = "INSERT INTO users (username, password) VALUES (?, ?)"
                                self.db_manager.execute_query(
                                    query, (username, hashed_password))
                            return True
                            except Exception as e:
                                self.logger.error(
                                    f"Failed to register user {username}: {str(e)}")
                            return False
