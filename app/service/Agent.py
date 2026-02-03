"""
AI Agent сервис с интеграцией MCP серверов
"""
import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.tools.calculator import add, subtract, multiply, divide, power, calculate_percentage
from app.utils.mock_llm import get_llm

# Настройка логирования
logger = logging.getLogger(__name__)

load_dotenv()

# Инициализация LLM модели (автоматически выбирает мок или реальную)
model = get_llm()

# Получаем абсолютные пути к MCP серверам
mcp_products_path = Path(__file__).parent.parent / "tools" / "MCP_test_task.py"
mcp_orders_path = Path(__file__).parent.parent / "tools" / "MCP_orders.py"

logger.info(f"Инициализация MCP клиента с серверами:")
logger.info(f"  - Products: {mcp_products_path}")
logger.info(f"  - Orders: {mcp_orders_path}")

# Инициализация MCP клиента с двумя серверами
client = MultiServerMCPClient(
    {
        "product_manager": {
            "command": "python",
            "args": [str(mcp_products_path)],
            "transport": "stdio",
        },
        "order_manager": {
            "command": "python",
            "args": [str(mcp_orders_path)],
            "transport": "stdio",
        },
    }
)


async def run_multi_server_agent(prompt: str) -> str:
    """
    Запуск AI агента с MCP серверами для обработки запроса
    
    Args:
        prompt: Текстовый запрос пользователя
        
    Returns:
        str: Ответ агента
        
    Raises:
        ValueError: При невалидном запросе
        Exception: При ошибке выполнения агента
        
    Examples:
        >>> await run_multi_server_agent("Покажи все продукты")
        "Вот список всех продуктов..."
    """
    try:
        logger.info(f"Начало обработки запроса: {prompt[:100]}...")
        
        # Получаем tools из MCP сервера
        logger.debug("Получение tools из MCP сервера")
        tools = await client.get_tools()
        logger.info(f"Получено {len(tools)} tools из MCP сервера")
        
        # Добавляем кастомные tools (калькулятор)
        custom_tools = [add, subtract, multiply, divide, power, calculate_percentage]
        tools += custom_tools
        logger.info(f"Добавлено {len(custom_tools)} кастомных tools")
        
        # Создаем агента
        logger.debug("Создание агента")
        agent = create_agent(model, tools)
        
        # Выполняем запрос
        logger.debug("Выполнение запроса агентом")
        response = await agent.ainvoke({
            "messages": prompt
        })
        
        result = response["messages"][-1].content
        logger.info("Запрос успешно обработан")
        logger.debug(f"Результат: {result[:100]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении агента: {str(e)}", exc_info=True)
        raise
