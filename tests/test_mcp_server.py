"""
Тесты для MCP сервера
"""
import pytest
import tempfile
import os
from pathlib import Path

# Импортируем классы из MCP сервера
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.tools.MCP_test_task import ProductManager, Product


class TestProductManager:
    """Тесты для ProductManager"""
    
    @pytest.fixture
    def temp_manager(self):
        """Фикстура для временного ProductManager"""
        # Создаем временную директорию
        temp_dir = tempfile.mkdtemp()
        
        # Сохраняем оригинальный путь и подменяем
        import app.tools.MCP_test_task as mcp_module
        original_init = ProductManager.__init__
        
        def temp_init(self):
            from app.db.database import Database
            db_path = Path(temp_dir) / "products.db"
            self.db = Database(str(db_path))
        
        ProductManager.__init__ = temp_init
        manager = ProductManager()
        
        yield manager
        
        # Восстанавливаем оригинальный __init__
        ProductManager.__init__ = original_init
        
        # Очистка
        db_path = Path(temp_dir) / "products.db"
        if os.path.exists(db_path):
            os.remove(db_path)
        os.rmdir(temp_dir)
    
    def test_get_all_products_empty(self, temp_manager):
        """Тест получения пустого списка продуктов"""
        products = temp_manager.get_all_products()
        assert isinstance(products, list)
        assert len(products) == 0
    
    def test_add_product(self, temp_manager):
        """Тест добавления продукта"""
        result = temp_manager.add_product(
            name="Test Product",
            price=999.99,
            category="Electronics",
            in_stock=True
        )
        
        assert result['name'] == "Test Product"
        assert result['price'] == 999.99
        assert result['category'] == "Electronics"
        assert result['in_stock'] == 1
        assert 'id' in result
    
    def test_add_product_negative_price(self, temp_manager):
        """Тест добавления продукта с отрицательной ценой"""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            temp_manager.add_product(
                name="Test",
                price=-100,
                category="Test",
                in_stock=True
            )
    
    def test_get_product_by_id(self, temp_manager):
        """Тест получения продукта по ID"""
        # Добавляем продукт
        added = temp_manager.add_product(
            name="iPhone",
            price=999,
            category="Electronics",
            in_stock=True
        )
        
        # Получаем по ID
        product = temp_manager.get_product_by_id(added['id'])
        
        assert product['id'] == added['id']
        assert product['name'] == "iPhone"
    
    def test_get_product_by_id_not_found(self, temp_manager):
        """Тест получения несуществующего продукта"""
        with pytest.raises(ValueError, match="Product with ID 999 not found"):
            temp_manager.get_product_by_id(999)
    
    def test_get_statistics_empty(self, temp_manager):
        """Тест статистики для пустой базы"""
        stats = temp_manager.get_statistics()
        
        assert stats['total_count'] == 0
        assert stats['average_price'] == 0
        assert stats['in_stock_count'] == 0
    
    def test_get_statistics_with_products(self, temp_manager):
        """Тест статистики с продуктами"""
        # Добавляем продукты
        temp_manager.add_product("Product 1", 100, "Cat A", True)
        temp_manager.add_product("Product 2", 200, "Cat B", True)
        temp_manager.add_product("Product 3", 300, "Cat A", False)
        
        stats = temp_manager.get_statistics()
        
        assert stats['total_count'] == 3
        assert stats['average_price'] == 200.0
        assert stats['in_stock_count'] == 2
    
    def test_get_all_products_with_data(self, temp_manager):
        """Тест получения всех продуктов"""
        # Добавляем продукты
        temp_manager.add_product("Product 1", 100, "Cat A", True)
        temp_manager.add_product("Product 2", 200, "Cat B", False)
        
        products = temp_manager.get_all_products()
        
        assert len(products) == 2
        assert products[0]['name'] == "Product 1"
        assert products[1]['name'] == "Product 2"


class TestProductModel:
    """Тесты для Pydantic модели Product"""
    
    def test_product_creation(self):
        """Тест создания продукта"""
        product = Product(
            id=1,
            name="Test",
            price=100.0,
            category="Electronics",
            in_stock=True
        )
        
        assert product.id == 1
        assert product.name == "Test"
        assert product.price == 100.0
        assert product.category == "Electronics"
        assert product.in_stock is True
    
    def test_product_validation(self):
        """Тест валидации полей"""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Product(
                id="not_an_int",  # Должно быть int
                name="Test",
                price=100.0,
                category="Electronics",
                in_stock=True
            )
