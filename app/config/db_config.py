from app.models.user import User
from app.config.base_config import BaseConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from bcrypt import hashpw, gensalt
from sqlalchemy.orm import Session

"""
Database configuration for BugHunter application.
Provides database connection settings and utilities.
"""

config = BaseConfig()

# Database URL from configuration with proper escaping
db_user = config.get_config_value("DB_USER", "")
db_password = quote_plus(str(config.get_config_value("DB_PASSWORD", "")))
db_host = config.get_config_value("DB_HOST", "")
db_port = config.get_config_value("DB_PORT", "")
db_name = config.get_config_value("DB_NAME", "")

# Construct connection string with proper escaping
DATABASE_URL = "postgresql://postgres:Qaz!Wsx@Edc#Rfv$@localhost:5432/bughunter_logincredentials"  # Ensure this URL is correct

# Create database engine
engine = create_engine(DATABASE_URL)

# Create configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin_user(_db: Session):
    """Create an admin user with a hashed password."""
    admin_username = "admin"
    admin_password = "StrongPassword123!"  # This should be a strong password
    hashed_password = hashpw(admin_password.encode("utf-8"), gensalt())

    # Check if the admin user already exists
    existing_user = _db.query(User).filter(User.username == admin_username).first()
    if not existing_user:
        new_user = User(username=admin_username, password_hash=hashed_password)
        _db.add(new_user)
        _db.commit()
        _db.refresh(new_user)
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    if some_condition:
        # some code
        value = some_function()
    elif another_condition:
        # some code
        value = another_function()
    else:
        # some code
        value = default_function()

def get_db():
    """Get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
