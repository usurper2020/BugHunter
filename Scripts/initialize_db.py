from app.services.database import DatabaseService
from app.models.user import User
from app.models.session import Session
from app.models.security_event import SecurityEvent
from app.models.login_attempt import LoginAttempt
from app.models.fingerprint import Fingerprint
from pathlib import Path
from datetime import datetime
import sys
import os
import logging
query = ""
message = ""
"""
Database initialization script for BugHunter application.
Creates all necessary tables and sets up initial data.
"""


# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

    def init_db():
        """Initialize the database schema"""
        try:
            # Create all tables
            Base.metadata.create_all(bind=engine)
            logging.info("Database tables created successfully")

            # Create a database session
            db = SessionLocal()
            try:
                # Create admin user with secure password
                create_admin_user(db)

                # Create initial security event for admin creation
                db_service = DatabaseService(db)
                admin_user = db_service.get_user_by_username("admin")

                db_service.create_security_event(
                    user_id=admin_user.id,
                    event_type="user_created",
                    event_data={
                        "username": "admin",
                        "created_at": datetime.utcnow().isoformat(),
                    },
                    severity=3,
                )
                logging.info(
                    "Admin user and security event created successfully")

                finally:
                    db.close()

                    except Exception as e:
                        logging.error(
                            f"Error initializing database: {str(e)}", exc_info=True)
                        raise

                        def verify_db():
                            """Verify database connection and schema"""
                            try:
                                # Create a test connection
                                db = SessionLocal()
                                try:
                                    # Test query
                                    db.execute("SELECT 1")
                                    logging.info(
                                        "Database connection verified successfully")

                                    # Verify tables exist
                                    tables = [
                                        User.__tablename__,
                                        Fingerprint.__tablename__,
                                        Session.__tablename__,
                                        LoginAttempt.__tablename__,
                                        SecurityEvent.__tablename__,
                                    ]

                                    for table in tables:
                                        result = db.execute(
                                            f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table}'"
                                        )
                                        if result.scalar():
                                            logging.info(
                                                f"Table '{table}' exists")
                                            else:
                                                logging.warning(
                                                    f"Table '{table}' not found")

                                                finally:
                                                    db.close()

                                                    except Exception as e:
                                                        logging.error(
                                                            f"Database verification failed: {str(e)}", exc_info=True)
                                                        raise

                                                        if __name__ == "__main__":
                                                            # Setup logging
                                                            logging.basic_config(
                                                                level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
                                                            )

                                                            try:
                                                                logging.info(
                                                                    "Starting database initialization...")
                                                                init_db()
                                                                logging.info(
                                                                    "Database initialization completed successfully")

                                                                logging.info(
                                                                    "Verifying database setup...")
                                                                verify_db()
                                                                logging.info(
                                                                    "Database verification completed successfully")

                                                                except Exception as e:
                                                                    logging.error(
                                                                        "Database initialization failed")
                                                                    sys.exit(1)

                                                                    sys.exit(0)
