from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
import os
import sys
from pathlib import Path

# Add project root directory to PYTHONPATH (for local execution)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import Database from app.db.database
try:
    from app.db.database import Database
except ImportError:
    # If import failed, add path explicitly
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
        
        # Define database path
        # In Docker: /app/data/products.db
        # Locally: project_root/data/products.db
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "data" / "products.db"
        self.db = Database(str(db_path))

    def get_all_products(self):
        """Returns the complete list of products"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_product_by_id(self, product_id: int):
        """Searches for product by ID. Raises ValueError if not found"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"Product with ID {product_id} not found")
            
            return dict(row)

    def add_product(self, name: str, price: float, category: str, in_stock: bool):
        """Add a new product with params (name, price, category, in_stock)"""
        # Validate data (price > 0)
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        # Add product to database
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (?, ?, ?, ?)",
                (name, price, category, 1 if in_stock else 0)
            )
            conn.commit()
            
            # Get ID of added product
            product_id = cursor.lastrowid
        
        # Return created product
        return self.get_product_by_id(product_id)

    def get_statistics(self):
        """Calculates total count and average price of products"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_count = cursor.fetchone()["count"]
            
            if total_count == 0:
                return {
                    "total_count": 0,
                    "average_price": 0,
                    "in_stock_count": 0
                }
            
            # Get average price
            cursor.execute("SELECT AVG(price) as avg_price FROM products")
            average_price = cursor.fetchone()["avg_price"]
            
            # Get count of items in stock
            cursor.execute("SELECT COUNT(*) as count FROM products WHERE in_stock = 1")
            in_stock_count = cursor.fetchone()["count"]
            
            return {
                "total_count": total_count,
                "average_price": round(average_price, 2),
                "in_stock_count": in_stock_count
            }


# Create the Products MCP server
mcp = FastMCP("Products")

manager = ProductManager()


# Define tools as regular functions
@mcp.tool()
def get_all_products():
    """Returns list of all products."""
    return manager.get_all_products()

@mcp.tool()
def add_new_product(name: str, price: float, category: str, in_stock: bool):
    """Adds a new product to the database. Returns the created product as a dictionary."""
    result = manager.add_product(name, price, category, in_stock)
    return {"success": True, "product": result}

@mcp.tool()
def get_product_by_id(product_id: int):
    """Searches for product by ID. Raises ValueError if not found"""
    return manager.get_product_by_id(product_id)

@mcp.tool()
def get_statistics():
    """Calculates total count and average price of products"""
    return manager.get_statistics()

if __name__ == "__main__":
    mcp.run()