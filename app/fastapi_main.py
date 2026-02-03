"""
FastAPI application for AI agent with MCP integration
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.agent.endpoints import router as agent_router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Agent API",
    description="API for working with AI agent with MCP integration for product management",
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

# Include routers
app.include_router(agent_router)


@app.get("/")
async def root():
    """
    Root endpoint with API information
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
    """Event on application startup"""
    logger.info("🚀 AI Agent API started")
    logger.info("📚 Documentation available at: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Event on application shutdown"""
    logger.info("🛑 AI Agent API stopped")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
