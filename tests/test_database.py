"""
Тесты для database модуля
"""
import pytest
import os
import tempfile
from pathlib import Path

from app.db.database import Database


class TestDatabase:
    """Тесты для класса Database"""
    
    @pytest.fixture
    def temp_db(self):
        """Фикстура для временной базы данных"""
        # Создаем временный файл
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        db = Database(db_path)
        yield db
        
        # Очистка после теста
        if os.path.exists(db_path):
            os.remove(db_path)
        os.rmdir(temp_dir)
    
    def test_database_creation(self, temp_db):
        """Тест создания базы данных"""
        assert os.path.exists(temp_db.db_path)
        
    def test_products_table_exists(self, temp_db):
        """Тест существования таблицы products"""
        with temp_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='products'
            """)
            result = cursor.fetchone()
            assert result is not None
            assert result['name'] == 'products'
    
    def test_insert_product(self, temp_db):
        """Тест добавления продукта"""
        with temp_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, price, category, in_stock)
                VALUES (?, ?, ?, ?)
            """, ("Test Product", 100.0, "Test", 1))
            conn.commit()
            
            # Проверяем что продукт добавлен
            cursor.execute("SELECT * FROM products WHERE name = ?", ("Test Product",))
            result = cursor.fetchone()
            
            assert result is not None
            assert result['name'] == "Test Product"
            assert result['price'] == 100.0
            assert result['category'] == "Test"
            assert result['in_stock'] == 1
    
    def test_select_products(self, temp_db):
        """Тест выборки продуктов"""
        with temp_db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Добавляем тестовые данные
            test_products = [
                ("Product 1", 100.0, "Category A", 1),
                ("Product 2", 200.0, "Category B", 0),
                ("Product 3", 300.0, "Category A", 1),
            ]
            
            cursor.executemany("""
                INSERT INTO products (name, price, category, in_stock)
                VALUES (?, ?, ?, ?)
            """, test_products)
            conn.commit()
            
            # Выбираем все продукты
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()
            
            assert len(results) == 3
            
    def test_context_manager(self, temp_db):
        """Тест работы context manager"""
        # Проверяем что connection закрывается после использования
        with temp_db.get_connection() as conn:
            assert conn is not None
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            
        # После выхода из контекста connection должен быть закрыт
        # (проверяем что нет исключений при создании нового подключения)
        with temp_db.get_connection() as conn2:
            assert conn2 is not None
    
    def test_row_factory(self, temp_db):
        """Тест работы row_factory для доступа по имени колонки"""
        with temp_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, price, category, in_stock)
                VALUES (?, ?, ?, ?)
            """, ("Test", 100.0, "Cat", 1))
            conn.commit()
            
            cursor.execute("SELECT * FROM products")
            row = cursor.fetchone()
            
            # Проверяем доступ по имени колонки
            assert row['name'] == "Test"
            assert row['price'] == 100.0
            assert row['category'] == "Cat"
            assert row['in_stock'] == 1
