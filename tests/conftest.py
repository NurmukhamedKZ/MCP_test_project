"""
Pytest конфигурация и общие фикстуры
"""
import pytest
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_env():
    """Фикстура для тестового окружения"""
    # Устанавливаем тестовые переменные окружения
    os.environ["OPENAI_API_KEY"] = "test-api-key"
    os.environ["PYTHONPATH"] = str(project_root)
    yield
    

@pytest.fixture
def mock_llm_response():
    """Фикстура для мокирования ответа LLM"""
    return "Вот список продуктов: iPhone 15, MacBook Pro"
