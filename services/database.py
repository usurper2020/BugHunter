"""
Database management service for the BugHunter application.
Handles database connections, sessions, and operations.
"""

import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.DatabaseManager')
        self.engine = None
        self.Session = None
        self.initialized = False
        
        # Ensure data directory exists
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def initialize(self) -> bool:
        """Initialize database connection and create tables"""
        try:
            db_path = self.data_dir / 'bughunter.db'
            self.engine = create_engine(f'sqlite:///{db_path}')
            self.Session = sessionmaker(bind=self.engine)
            
            # Create all tables
            Base.metadata.create_all(self.engine)
            
            self.initialized = True
            self.logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            return False
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session"""
        if not self.initialized:
            raise Exception("Database not initialized")
        
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[dict] = None) -> list:
        """Execute a raw SQL query"""
        try:
            with self.get_session() as session:
                result = session.execute(query, params or {})
                return result.fetchall()
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the database"""
        try:
            if not backup_path:
                backup_dir = Path('backups')
                backup_dir.mkdir(exist_ok=True)
                backup_path = backup_dir / f'bughunter_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            
            # Create backup using SQLite's backup API
            with self.get_session() as session:
                session.execute('VACUUM INTO ?', [str(backup_path)])
            
            self.logger.info(f"Database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Database backup failed: {str(e)}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Close current connections
            self.engine.dispose()
            
            # Replace current database with backup
            db_path = self.data_dir / 'bughunter.db'
            import shutil
            shutil.copy2(backup_file, db_path)
            
            # Reinitialize database connection
            self.initialize()
            
            self.logger.info(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Database restore failed: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup database resources"""
        try:
            if self.engine:
                self.engine.dispose()
            self.initialized = False
            self.logger.info("Database resources cleaned up")
        except Exception as e:
            self.logger.error(f"Database cleanup failed: {str(e)}")
