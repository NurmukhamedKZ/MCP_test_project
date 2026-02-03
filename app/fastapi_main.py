from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Add parent directory to path to import ProductManager
sys.path.append(str(Path(__file__).parent.parent))

from app.service.Agent import run_multi_server_agent


app = FastAPI(
    title="Product Manager API",
    description="Simple API to test ProductManager functionality",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Root endpoint with API info"""
    return {
        "message": "Welcome to Product Manager API",
    }


@app.post("/ask_agent")
async def add_product(prompt: str):
    """Add a new product"""
    try:
        response = await run_multi_server_agent(prompt)
        return response,
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
