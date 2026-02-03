"""
Mock LLM для тестирования без реального API ключа
"""
import logging
from typing import Any, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun

logger = logging.getLogger(__name__)


class MockChatModel(BaseChatModel):
    """
    Mock реализация ChatModel для тестирования без реального API
    
    Использует простые правила для генерации ответов на основе запроса.
    """
    
    model_name: str = "mock-model"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Генерация мок-ответа
        
        Args:
            messages: Список сообщений
            stop: Токены остановки
            run_manager: Менеджер callback'ов
            
        Returns:
            ChatResult: Результат с мок-ответом
        """
        last_message = messages[-1].content.lower() if messages else ""
        
        logger.info(f"MockLLM получил запрос: {last_message[:100]}")
        
        # Простая логика для генерации ответов
        if "продукт" in last_message or "товар" in last_message:
            if "все" in last_message or "список" in last_message:
                response = "Я использую инструмент get_all_products для получения списка всех продуктов."
            elif "добав" in last_message:
                response = "Я использую инструмент add_new_product для добавления нового продукта."
            elif "найд" in last_message or "поиск" in last_message:
                response = "Я использую инструмент get_product_by_id для поиска продукта."
            else:
                response = "Я помогу вам с продуктами. Используйте инструменты для работы с продуктами."
        
        elif "заказ" in last_message:
            if "создать" in last_message or "сделать" in last_message:
                response = "Я использую инструмент create_order для создания заказа."
            elif "список" in last_message or "все" in last_message:
                response = "Я использую инструмент list_orders для получения списка заказов."
            elif "статус" in last_message:
                response = "Я использую инструмент update_order_status для обновления статуса заказа."
            else:
                response = "Я помогу вам с заказами. Используйте инструменты для работы с заказами."
        
        elif "статистик" in last_message:
            response = "Я использую инструмент get_statistics для получения статистики."
        
        elif "calculate" in last_message or "считай" in last_message or "вычисл" in last_message:
            response = "Я использую калькулятор для вычислений."
        
        else:
            response = "Я - AI ассистент для управления продуктами и заказами. Чем могу помочь?"
        
        logger.info(f"MockLLM сгенерировал ответ: {response[:100]}")
        
        message = AIMessage(content=response)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])
    
    @property
    def _llm_type(self) -> str:
        """Тип LLM"""
        return "mock-chat-model"
    
    @property
    def _identifying_params(self) -> dict:
        """Параметры для идентификации"""
        return {"model_name": self.model_name}


def get_llm(use_mock: bool = False) -> BaseChatModel:
    """
    Фабрика для получения LLM модели
    
    Args:
        use_mock: Использовать ли мок LLM вместо реального
        
    Returns:
        BaseChatModel: LLM модель (реальная или мок)
        
    Examples:
        >>> llm = get_llm(use_mock=True)  # Для тестов
        >>> llm = get_llm(use_mock=False)  # Для продакшена
    """
    import os
    from langchain_openai import ChatOpenAI
    
    if use_mock or not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "test-api-key":
        logger.info("Использование Mock LLM")
        return MockChatModel()
    else:
        logger.info("Использование OpenAI LLM")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
