import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"
    TRANSPORT_PROTO = "streamable_http"
    server_name = "Math"
    servers = {server_name: {"url": SERVER_URL, "transport": TRANSPORT_PROTO}}
    MODEL = "gemini-2.0-flash"
    model = ChatVertexAI(model_name=MODEL)

    client = MultiServerMCPClient(servers)

    session_cm = client.session(server_name)
    session = await session_cm.__aenter__()

    tools_catalog = await client.get_tools()
    model_with_tools = model.bind_tools(tools_catalog)

    prompt = "add 10 and 20"
    hmsg = HumanMessage(content=prompt)

    print(f"Agent->Prompting Model :{prompt}")
    tc = model_with_tools.invoke([hmsg])

    print(f"Agent->Got response from Model")

    for t in tc.tool_calls:
        tname = t['name']
        targs = t['args']
        print(f"Agent->Invoking tool :{tname} with args :{targs}")

        result = await session.call_tool(name=tname, arguments=targs)
        print(f"Agent->Got Results :{result.content[0].text}")

    await session_cm.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main())
