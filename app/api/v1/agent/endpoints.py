"""
API endpoints for working with AI agent
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.service.Agent import run_multi_server_agent

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


class QueryRequest(BaseModel):
    """Agent query request model"""
    query: str = Field(..., description="User query to the agent", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show all products"
            }
        }


class QueryResponse(BaseModel):
    """Agent response model"""
    result: str = Field(..., description="Query execution result")
    status: str = Field(default="success", description="Execution status")
    error: Optional[str] = Field(None, description="Error description, if any")
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Here is the list of all products...",
                "status": "success",
                "error": None
            }
        }


@router.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest) -> QueryResponse:
    """
    Send query to AI agent
    
    Args:
        request: Request with text for the agent
        
    Returns:
        QueryResponse: Agent response with result
        
    Raises:
        HTTPException: On request processing error
        
    Examples:
        ```json
        POST /api/v1/agent/query
        {
            "query": "Show all products in Electronics category"
        }
        ```
    """
    try:
        logger.info(f"Received agent query: {request.query[:100]}...")
        
        # Run agent
        result = await run_multi_server_agent(request.query)
        
        logger.info("Query processed successfully")
        
        return QueryResponse(
            result=result,
            status="success"
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """
    Check API health status
    
    Returns:
        dict: Service status
    """
    logger.debug("Health check request")
    return {
        "status": "healthy",
        "service": "AI Agent API",
        "version": "1.0.0"
    }
