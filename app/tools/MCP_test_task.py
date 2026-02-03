from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH (для локального запуска)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Импортируем Database из app.db.database
try:
    from app.db.database import Database
except ImportError:
    # Если импорт не удался, добавляем путь явно
    import importlib.util
    db_module_path = project_root / "app" / "db" / "database.py"
    spec = importlib.util.spec_from_file_location("database", db_module_path)
    database_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database_module)
    Database = database_module.Database


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool


class ProductManager:
    def __init__(self):
        """Initialize ProductManager with SQLite database"""
        
        # Определяем путь к базе данных
        # В Docker: /app/data/products.db
        # Локально: project_root/data/products.db
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "data" / "products.db"
        self.db = Database(str(db_path))

    def get_all_products(self):
        """Возвращает весь список продуктов"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_product_by_id(self, product_id: int):
        """Ищет продукт по ID. Если не найден — выбрасывает ValueError"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"Product with ID {product_id} not found")
            
            return dict(row)

    def add_product(self, name: str, price: float, category: str, in_stock: bool):
        """Add a new product with params (name, price, category, in_stock)"""
        # Валидирует данные (цена > 0)
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        # Добавляем продукт в базу данных
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (?, ?, ?, ?)",
                (name, price, category, 1 if in_stock else 0)
            )
            conn.commit()
            
            # Получаем ID добавленного продукта
            product_id = cursor.lastrowid
        
        # Возвращаем созданный продукт
        return self.get_product_by_id(product_id)

    def get_statistics(self):
        """Считает общее кол-во и среднюю цену продуктов"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем общее количество
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_count = cursor.fetchone()["count"]
            
            if total_count == 0:
                return {
                    "total_count": 0,
                    "average_price": 0,
                    "in_stock_count": 0
                }
            
            # Получаем среднюю цену
            cursor.execute("SELECT AVG(price) as avg_price FROM products")
            average_price = cursor.fetchone()["avg_price"]
            
            # Получаем количество товаров в наличии
            cursor.execute("SELECT COUNT(*) as count FROM products WHERE in_stock = 1")
            in_stock_count = cursor.fetchone()["count"]
            
            return {
                "total_count": total_count,
                "average_price": round(average_price, 2),
                "in_stock_count": in_stock_count
            }


# Create the Calculator MCP server
mcp = FastMCP("Products")

manager = ProductManager()


# 2. Описываем инструменты как обычные функции
@mcp.tool()
def get_all_products():
    """Возвращает список всех продуктов."""
    return manager.get_all_products()

@mcp.tool()
def add_new_product(name: str, price: float, category: str, in_stock: bool):
    """Добавляет новый продукт в базу. Returns the created product as a dictionary."""
    result = manager.add_product(name, price, category, in_stock)
    return {"success": True, "product": result}

@mcp.tool()
def get_product_by_id(product_id: int):
    """Ищет продукт по ID. Если не найден — выбрасывает ValueError"""
    return manager.get_product_by_id(product_id)

@mcp.tool()
def get_statistics():
    """Считает общее кол-во и среднюю цену продуктов"""
    return manager.get_statistics()

if __name__ == "__main__":
    mcp.run()