"""
SQLite database manager for working with products
"""
import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Generator
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database manager for working with products
    
    Attributes:
        db_path (str): Path to database file
        
    Examples:
        >>> db = Database("data/products.db")
        >>> with db.get_connection() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT * FROM products")
    """
    
    def __init__(self, db_path: str):
        """
        Initialize database
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        logger.info(f"Initializing database: {db_path}")
        
        # Create directory for database if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created directory for DB: {db_dir}")
        
        self._init_db()
    
    def _init_db(self) -> None:
        """
        Initialize database tables
        
        Creates products table if it doesn't exist
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        category TEXT NOT NULL,
                        in_stock INTEGER NOT NULL
                    )
                """)
                conn.commit()
                logger.info("Products table initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing DB: {str(e)}", exc_info=True)
            raise
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager for working with DB connection
        
        Yields:
            sqlite3.Connection: Database connection
            
        Examples:
            >>> with db.get_connection() as conn:
            ...     cursor = conn.cursor()
            ...     cursor.execute("SELECT * FROM products")
        """
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        except Exception as e:
            logger.error(f"Error working with DB: {str(e)}")
            raise
        finally:
            conn.close()
