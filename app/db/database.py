import sqlite3
import os
from contextlib import contextmanager
from typing import Generator
from pathlib import Path


class Database:
    """Simple SQLite database manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
        # Создаем директорию для базы данных, если её нет
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        self._init_db()
    
    def _init_db(self):
        """Initialize database with products table"""
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
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
