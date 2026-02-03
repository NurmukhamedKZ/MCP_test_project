"""
SQLite database manager для работы с продуктами
"""
import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Generator
from pathlib import Path

# Настройка логирования
logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database manager для работы с продуктами
    
    Attributes:
        db_path (str): Путь к файлу базы данных
        
    Examples:
        >>> db = Database("data/products.db")
        >>> with db.get_connection() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT * FROM products")
    """
    
    def __init__(self, db_path: str):
        """
        Инициализация базы данных
        
        Args:
            db_path: Путь к файлу SQLite базы данных
        """
        self.db_path = db_path
        logger.info(f"Инициализация базы данных: {db_path}")
        
        # Создаем директорию для базы данных, если её нет
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Создана директория для БД: {db_dir}")
        
        self._init_db()
    
    def _init_db(self) -> None:
        """
        Инициализация таблиц базы данных
        
        Создает таблицу products если она не существует
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
                logger.info("Таблица products успешно инициализирована")
        except Exception as e:
            logger.error(f"Ошибка при инициализации БД: {str(e)}", exc_info=True)
            raise
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager для работы с подключением к БД
        
        Yields:
            sqlite3.Connection: Подключение к базе данных
            
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
            logger.error(f"Ошибка при работе с БД: {str(e)}")
            raise
        finally:
            conn.close()
