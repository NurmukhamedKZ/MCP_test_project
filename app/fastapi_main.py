"""
FastAPI приложение для AI агента с MCP интеграцией
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.agent.endpoints import router as agent_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="AI Agent API",
    description="API для работы с AI агентом с MCP интеграцией для управления продуктами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(agent_router)


@app.get("/")
async def root():
    """
    Корневой endpoint с информацией об API
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "query_agent": "POST /api/v1/agent/query",
            "health_check": "GET /api/v1/agent/health"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Событие при запуске приложения"""
    logger.info("🚀 AI Agent API запущен")
    logger.info("📚 Документация доступна по адресу: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Событие при остановке приложения"""
    logger.info("🛑 AI Agent API остановлен")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
