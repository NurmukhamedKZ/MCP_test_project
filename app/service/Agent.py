import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import HumanMessage

from app.tools.calculator import add, subtract, multiply, divide, power, calculate_percentage

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Получаем абсолютный путь к MCP серверу
mcp_script_path = Path(__file__).parent.parent / "tools" / "MCP_test_task.py"

client = MultiServerMCPClient(
    {
        "product_manager": {
            "command": "python",
            "args": [str(mcp_script_path)],
            "transport": "stdio",
        },
    }
)


async def run_multi_server_agent(prompt: str):
    """Create and run agent with multiple MCP servers"""

    tools = await client.get_tools()

    tools += [add, subtract, multiply, divide, power, calculate_percentage]


    agent = create_agent(model, tools)


    response = await agent.ainvoke({
        "messages": prompt
    })

    return response["messages"][-1].content
