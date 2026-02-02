import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"
    TRANSPORT_PROTO = "streamable_http"
    server_name = "Math"
    servers = {server_name: {"url": SERVER_URL, "transport": TRANSPORT_PROTO}}

    client = MultiServerMCPClient(servers)
    session_cm = client.session(server_name)
    session = await session_cm.__aenter__()

    tool_name = "add_numbers"
    args = {"a": 6, "b": 10}
    print(f"Invoking tool :'{tool_name}', with arguments :{args}")
    result = await session.call_tool(name=tool_name, arguments=args)
    print(f"Result :{result.content[0].text}")
    
    await session_cm.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main())
