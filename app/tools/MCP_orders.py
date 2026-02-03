"""
MCP server for working with orders
Bonus task: second MCP server
"""
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

# Add project root directory to PYTHONPATH
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import Database
try:
    from app.db.database import Database
except ImportError:
    import importlib.util
    db_module_path = project_root / "app" / "db" / "database.py"
    spec = importlib.util.spec_from_file_location("database", db_module_path)
    database_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database_module)
    Database = database_module.Database

# Setup logging
logger = logging.getLogger(__name__)


class Order(BaseModel):
    """Order model"""
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: str  # pending, completed, cancelled
    created_at: str


class OrderManager:
    """Manager for working with orders"""
    
    def __init__(self):
        """Initialize OrderManager with SQLite database"""
        logger.info("Initializing OrderManager")
        
        # Define database path
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "data" / "products.db"
        self.db = Database(str(db_path))
        
        # Create orders table
        self._init_orders_table()
    
    def _init_orders_table(self) -> None:
        """Create orders table"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        total_price REAL NOT NULL,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                """)
                conn.commit()
                logger.info("Orders table initialized successfully")
        except Exception as e:
            logger.error(f"Error creating orders table: {str(e)}")
            raise
    
    def create_order(self, product_id: int, quantity: int) -> Dict:
        """
        Create order for product
        
        Args:
            product_id: Product ID
            quantity: Quantity
            
        Returns:
            Dict: Created order
            
        Raises:
            ValueError: If product not found or out of stock
        """
        logger.info(f"Creating order: product_id={product_id}, quantity={quantity}")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check product existence
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")
            
            if not product['in_stock']:
                raise ValueError(f"Product {product['name']} is out of stock")
            
            # Calculate total price
            total_price = product['price'] * quantity
            created_at = datetime.now().isoformat()
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (product_id, quantity, total_price, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, quantity, total_price, "pending", created_at))
            conn.commit()
            
            order_id = cursor.lastrowid
            logger.info(f"Order created with ID: {order_id}")
        
        return self.get_order_by_id(order_id)
    
    def get_order_by_id(self, order_id: int) -> Dict:
        """Get order by ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                raise ValueError(f"Order with ID {order_id} not found")
            
            return dict(order)
    
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
            orders = cursor.fetchall()
            return [dict(order) for order in orders]
    
    def update_order_status(self, order_id: int, status: str) -> Dict:
        """
        Update order status
        
        Args:
            order_id: Order ID
            status: New status (pending, completed, cancelled)
        """
        valid_statuses = ["pending", "completed", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check order existence
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise ValueError(f"Order with ID {order_id} not found")
            
            # Update status
            cursor.execute("""
                UPDATE orders SET status = ? WHERE id = ?
            """, (status, order_id))
            conn.commit()
            
            logger.info(f"Order {order_id} status updated to {status}")
        
        return self.get_order_by_id(order_id)
    
    def get_order_statistics(self) -> Dict:
        """Get order statistics"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total order count
            cursor.execute("SELECT COUNT(*) as count FROM orders")
            total_orders = cursor.fetchone()["count"]
            
            # Total order sum
            cursor.execute("SELECT SUM(total_price) as total FROM orders")
            total_revenue = cursor.fetchone()["total"] or 0
            
            # Count by status
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)
            status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
            
            return {
                "total_orders": total_orders,
                "total_revenue": round(total_revenue, 2),
                "pending_orders": status_counts.get("pending", 0),
                "completed_orders": status_counts.get("completed", 0),
                "cancelled_orders": status_counts.get("cancelled", 0)
            }


# Create MCP server for orders
mcp = FastMCP("Orders")

manager = OrderManager()


@mcp.tool()
def create_order(product_id: int, quantity: int):
    """
    Create new order for product
    
    Args:
        product_id: Product ID for order
        quantity: Quantity of items
        
    Returns:
        dict: Information about created order
    """
    result = manager.create_order(product_id, quantity)
    return {"success": True, "order": result}


@mcp.tool()
def get_order(order_id: int):
    """
    Get order information by ID
    
    Args:
        order_id: Order ID
    """
    return manager.get_order_by_id(order_id)


@mcp.tool()
def list_orders():
    """Get list of all orders"""
    return manager.get_all_orders()


@mcp.tool()
def update_order_status(order_id: int, status: str):
    """
    Update order status
    
    Args:
        order_id: Order ID
        status: New status (pending, completed, cancelled)
    """
    result = manager.update_order_status(order_id, status)
    return {"success": True, "order": result}


@mcp.tool()
def get_order_statistics():
    """Get order statistics"""
    return manager.get_order_statistics()


if __name__ == "__main__":
    mcp.run()
