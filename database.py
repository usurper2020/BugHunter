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
    """Manage database connections and operations"""
    
    @staticmethod
    @contextmanager
    def get_session() -> Generator:
        """Get a database session with automatic cleanup"""
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
        """Initialize the database schema"""
        try:
            Base.metadata.create_all(engine)
            logger.info("Database schema initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def drop_db() -> None:
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(engine)
            logger.info("Database schema dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database schema: {str(e)}", exc_info=True)
            raise

class CacheManager:
    """Manage Redis caching operations"""
    
    @staticmethod
    def get(key: str) -> str:
        """Get a value from cache"""
        try:
            return redis_client.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def set(key: str, value: str, expire: int = None) -> bool:
        """Set a value in cache with optional expiration"""
        try:
            if expire is None:
                expire = config.get('CACHE_TTL_MINUTES') * 60
            return redis_client.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete a value from cache"""
        try:
            return redis_client.delete(key) > 0
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def flush() -> bool:
        """Flush all cache entries (use with caution!)"""
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
