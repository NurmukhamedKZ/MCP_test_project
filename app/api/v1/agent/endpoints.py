"""
API endpoints для работы с AI агентом
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.service.Agent import run_multi_server_agent

# Настройка логирования
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


class QueryRequest(BaseModel):
    """Модель запроса к агенту"""
    query: str = Field(..., description="Запрос пользователя к агенту", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Покажи все продукты"
            }
        }


class QueryResponse(BaseModel):
    """Модель ответа агента"""
    result: str = Field(..., description="Результат выполнения запроса")
    status: str = Field(default="success", description="Статус выполнения")
    error: Optional[str] = Field(None, description="Описание ошибки, если есть")
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Вот список всех продуктов...",
                "status": "success",
                "error": None
            }
        }


@router.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest) -> QueryResponse:
    """
    Отправить запрос AI агенту
    
    Args:
        request: Запрос с текстом для агента
        
    Returns:
        QueryResponse: Ответ агента с результатом
        
    Raises:
        HTTPException: При ошибке обработки запроса
        
    Examples:
        ```json
        POST /api/v1/agent/query
        {
            "query": "Покажи все продукты в категории Электроника"
        }
        ```
    """
    try:
        logger.info(f"Получен запрос к агенту: {request.query[:100]}...")
        
        # Запускаем агента
        result = await run_multi_server_agent(request.query)
        
        logger.info("Запрос успешно обработан")
        
        return QueryResponse(
            result=result,
            status="success"
        )
        
    except ValueError as e:
        logger.error(f"Ошибка валидации: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке запроса: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """
    Проверка работоспособности API
    
    Returns:
        dict: Статус сервиса
    """
    logger.debug("Health check запрос")
    return {
        "status": "healthy",
        "service": "AI Agent API",
        "version": "1.0.0"
    }
