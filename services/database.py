from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import redis

from config import config
from logger_config import logger_config

logger = logger_config.get_logger(__name__)

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    config.get_database_url(),
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)

# Create session factory
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

# Create declarative base for models
Base = declarative_base()

# Create Redis connection
redis_client = redis.from_url(config.get_redis_url())

class DatabaseManager:
    """
    Manage database connections and operations in the BugHunter application.
    
    This class provides static methods for:
    - Managing database sessions with automatic cleanup
    - Initializing and dropping database schemas
    - Handling transaction management
    
    Uses SQLAlchemy for database operations with connection pooling
    configured for optimal performance.
    """
    
    @staticmethod
    @contextmanager
    def get_session() -> Generator:
        """
        Get a database session with automatic cleanup using context management.
        
        This method provides a session that will automatically:
        - Commit changes on successful execution
        - Rollback changes on exception
        - Close the session when finished
        
        Yields:
            Session: An SQLAlchemy session object
            
        Raises:
            Exception: Any database-related exceptions that occur during operations
            
        Example:
            with DatabaseManager.get_session() as session:
                user = session.query(User).filter_by(id=1).first()
        """
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise
        finally:
            session.close()
    
    @staticmethod
    def init_db() -> None:
        """
        Initialize the database schema.
        
        Creates all tables defined in SQLAlchemy models.
        Should be called when setting up the application
        for the first time or after dropping the schema.
        
        Raises:
            Exception: If schema initialization fails
        """
        try:
            Base.metadata.create_all(engine)
            logger.info("Database schema initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def drop_db() -> None:
        """
        Drop all database tables and schema.
        
        WARNING: This operation is destructive and will delete all data.
        Should only be used in development or when resetting the application.
        
        Raises:
            Exception: If schema deletion fails
        """
        try:
            Base.metadata.drop_all(engine)
            logger.info("Database schema dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database schema: {str(e)}", exc_info=True)
            raise

class CacheManager:
    """
    Manage Redis caching operations in the BugHunter application.
    
    This class provides static methods for:
    - Getting and setting cached values
    - Deleting cache entries
    - Flushing the entire cache
    
    Uses Redis for fast in-memory caching with optional expiration times.
    """
    
    @staticmethod
    def get(key: str) -> str:
        """
        Retrieve a value from the Redis cache.
        
        Parameters:
            key (str): The cache key to retrieve
            
        Returns:
            str: The cached value if found, None otherwise
            
        Raises:
            Exception: If cache retrieval fails (logged and returns None)
        """
        try:
            return redis_client.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def set(key: str, value: str, expire: int = None) -> bool:
        """
        Store a value in the Redis cache.
        
        Parameters:
            key (str): The cache key to store
            value (str): The value to cache
            expire (int, optional): Time in seconds until the key expires.
                                  If None, uses default from config
                                  
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            Exception: If cache storage fails (logged and returns False)
        """
        try:
            if expire is None:
                expire = config.get('CACHE_TTL_MINUTES') * 60
            return redis_client.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Remove a value from the Redis cache.
        
        Parameters:
            key (str): The cache key to delete
            
        Returns:
            bool: True if key was deleted, False if key didn't exist
                 or deletion failed
            
        Raises:
            Exception: If cache deletion fails (logged and returns False)
        """
        try:
            return redis_client.delete(key) > 0
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def flush() -> bool:
        """
        Remove all entries from the Redis cache.
        
        WARNING: This operation is destructive and will delete all cached data.
        Should only be used when a complete cache reset is needed.
        
        Returns:
            bool: True if flush was successful, False otherwise
            
        Raises:
            Exception: If cache flush fails (logged and returns False)
        """
        try:
            return redis_client.flushall()
        except Exception as e:
            logger.error(f"Cache flush error: {str(e)}", exc_info=True)
            return False

# Example usage:
# with DatabaseManager.get_session() as session:
#     try:
#         # Perform database operations
#         user = session.query(User).filter_by(id=1).first()
#         # Session will be automatically committed if no exceptions occur
#     except Exception as e:
#         # Session will be automatically rolled back on exception
#         logger.error(f"Error querying user: {str(e)}")
#         raise

# Example cache usage:
# cache_key = f"user_{user_id}"
# user_data = CacheManager.get(cache_key)
# if not user_data:
#     with DatabaseManager.get_session() as session:
#         user = session.query(User).filter_by(id=user_id).first()
#         if user:
#             CacheManager.set(cache_key, user.to_json())
