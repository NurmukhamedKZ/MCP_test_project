"""
AI Agent service with MCP servers integration
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

# Setup logging
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize LLM model (automatically chooses mock or real)
model = get_llm()

# Get absolute paths to MCP servers
mcp_products_path = Path(__file__).parent.parent / "tools" / "MCP_test_task.py"
mcp_orders_path = Path(__file__).parent.parent / "tools" / "MCP_orders.py"

logger.info(f"Initializing MCP client with servers:")
logger.info(f"  - Products: {mcp_products_path}")
logger.info(f"  - Orders: {mcp_orders_path}")

# Initialize MCP client with two servers
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
    Run AI agent with MCP servers to process query
    
    Args:
        prompt: User text query
        
    Returns:
        str: Agent response
        
    Raises:
        ValueError: On invalid query
        Exception: On agent execution error
        
    Examples:
        >>> await run_multi_server_agent("Show all products")
        "Here is the list of all products..."
    """
    try:
        logger.info(f"Starting query processing: {prompt[:100]}...")
        
        # Get tools from MCP server
        logger.debug("Getting tools from MCP server")
        tools = await client.get_tools()
        logger.info(f"Retrieved {len(tools)} tools from MCP server")
        
        # Add custom tools (calculator)
        custom_tools = [add, subtract, multiply, divide, power, calculate_percentage]
        tools += custom_tools
        logger.info(f"Added {len(custom_tools)} custom tools")
        
        # Create agent
        logger.debug("Creating agent")
        agent = create_agent(model, tools)
        
        # Execute query
        logger.debug("Executing query with agent")
        response = await agent.ainvoke({
            "messages": prompt
        })
        
        result = response["messages"][-1].content
        logger.info("Query processed successfully")
        logger.debug(f"Result: {result[:100]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing agent: {str(e)}", exc_info=True)
        raise
