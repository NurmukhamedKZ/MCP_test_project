"""
Mock LLM for testing without real API key
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
    Mock ChatModel implementation for testing without real API
    
    Uses simple rules to generate responses based on query.
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
        Generate mock response
        
        Args:
            messages: List of messages
            stop: Stop tokens
            run_manager: Callback manager
            
        Returns:
            ChatResult: Result with mock response
        """
        last_message = messages[-1].content.lower() if messages else ""
        
        logger.info(f"MockLLM received query: {last_message[:100]}")
        
        # Simple logic for generating responses
        if "product" in last_message or "item" in last_message:
            if "all" in last_message or "list" in last_message:
                response = "I'm using get_all_products tool to retrieve the list of all products."
            elif "add" in last_message:
                response = "I'm using add_new_product tool to add a new product."
            elif "find" in last_message or "search" in last_message:
                response = "I'm using get_product_by_id tool to search for product."
            else:
                response = "I'll help you with products. Use tools to work with products."
        
        elif "order" in last_message:
            if "create" in last_message or "make" in last_message:
                response = "I'm using create_order tool to create order."
            elif "list" in last_message or "all" in last_message:
                response = "I'm using list_orders tool to get list of orders."
            elif "status" in last_message:
                response = "I'm using update_order_status tool to update order status."
            else:
                response = "I'll help you with orders. Use tools to work with orders."
        
        elif "statistic" in last_message:
            response = "I'm using get_statistics tool to get statistics."
        
        elif "calculate" in last_message or "compute" in last_message:
            response = "I'm using calculator for calculations."
        
        else:
            response = "I'm an AI assistant for managing products and orders. How can I help?"
        
        logger.info(f"MockLLM generated response: {response[:100]}")
        
        message = AIMessage(content=response)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])
    
    @property
    def _llm_type(self) -> str:
        """LLM type"""
        return "mock-chat-model"
    
    @property
    def _identifying_params(self) -> dict:
        """Identifying parameters"""
        return {"model_name": self.model_name}


def get_llm(use_mock: bool = False) -> BaseChatModel:
    """
    Factory to get LLM model
    
    Args:
        use_mock: Whether to use mock LLM instead of real one
        
    Returns:
        BaseChatModel: LLM model (real or mock)
        
    Examples:
        >>> llm = get_llm(use_mock=True)  # For tests
        >>> llm = get_llm(use_mock=False)  # For production
    """
    import os
    from langchain_openai import ChatOpenAI
    
    if use_mock or not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "test-api-key":
        logger.info("Using Mock LLM")
        return MockChatModel()
    else:
        logger.info("Using OpenAI LLM")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
