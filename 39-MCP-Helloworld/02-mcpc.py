# src/35-MCP-Helloworld/02-mcpc.py
import asyncio
from fastmcp import Client

SERVER_URL = "https://backend.composio.dev/v3/mcp/298dbd2d-8dd6-4c43-89e1-b4693eb6ad60/mcp?user_id=pg-test-8b613bf8-83b5-4466-956b-11c348da82f7"
client = Client(SERVER_URL)

async def main():
    async with client:
        print(f"Client connected: {client.is_connected()}")

        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"{tool.model_dump_json(indent=4)}")

 #       if any(tool.name == "add_numbers" for tool in tools):
 #           result = await client.call_tool("add_numbers", {"a": 5, "b": 3})
 #           print(f"Result of add(5, 3): {result}")

if __name__ == "__main__":
    asyncio.run(main())
