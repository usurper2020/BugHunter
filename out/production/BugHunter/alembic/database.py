from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
import logging
import contextlib
default = None
value = None
k = 10
context = {}

# Database URL from environment or default


# Configure logging
logging.basic_config(level=logging.INFO)
logger = logging.get_logger(__name__)

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./test.db"  # Set a default value or comment out the check
)
# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# if not SQLALCHEMY_DATABASE_URL:
#     logger.error("SQLALCHEMY_DATABASE_URL environment variable not set")
#     raise RuntimeError("SQLALCHEMY_DATABASE_URL environment variable not set")

# Remove the breakpoint to avoid pausing execution
# breakpoint()

engine = create_engine(
     SQLALCHEMY_DATABASE_URL,
     echo=os.getenv("SQLALCHEMY_ECHO", "False").lower() in ("true", "1"),
     )

 # Configure logging
 logging.basic_config(level=logging.INFO)
  logger = logging.get_logger(__name__)

   try:
        # Test the connection
        with engine.connect() as connection:
            # Breakpoint to verify connection
    breakpoint()
    pass
    except Exception as e:
        raise RuntimeError(f"Error connecting to the database: {e}")

        # Create a configured "Session" class
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)
        # Create a Base class for declarative class definitions
        Base = declarative_base()

        @contextlib.contextmanager
        def get_db():
            """Dependency to get database session.

                    Yields:
                    db: SQLAlchemy session object.
                    """
            db = SessionLocal()
             try:
                  # Breakpoint before yielding session
                breakpoint()
                yield db
                finally:
                    db.close()
                    # Breakpoint after closing session
                breakpoint()
