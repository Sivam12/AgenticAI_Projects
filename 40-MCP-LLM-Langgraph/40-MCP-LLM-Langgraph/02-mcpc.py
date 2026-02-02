import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"

    client_ctx = streamablehttp_client(SERVER_URL)
    r, w, _ = await client_ctx.__aenter__()

    session = ClientSession(r, w)
    await session.__aenter__()

    await session.initialize()

    tool_name = "add_numbers"
    args = {"a": 6, "b": 10}
    print(f"Invoke tool :'{tool_name}' with args :{args}")

    result = await session.call_tool(tool_name, arguments=args)
    print(result.content[0].text)

    await session.__aexit__(None, None, None)
    await client_ctx.__aexit__(None, None, None)
    
if __name__ == "__main__":
    asyncio.run(main())

