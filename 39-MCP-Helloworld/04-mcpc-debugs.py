# src/35-MCP-Helloworld/02-mcpc.py
import asyncio
from fastmcp import Client
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MCPHelloWorld")

SERVER_URL = "http://127.0.0.1:3333/mcp/"
client = Client(SERVER_URL)

async def main():
    async with client:
        result = await client.call_tool("add_numbers", {"a": 5, "b": 3})
        print(f"Result of add_numbers(5, 3): {result}")

if __name__ == "__main__":
    asyncio.run(main())
