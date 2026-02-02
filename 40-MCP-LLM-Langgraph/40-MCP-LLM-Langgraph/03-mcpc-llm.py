import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage

from langchain_mcp_adapters.tools import load_mcp_tools

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"
    MODEL = "gemini-2.0-flash"
    llm = ChatVertexAI(model_name=MODEL)

    client_ctx = streamablehttp_client(SERVER_URL)
    r, w, _ = await client_ctx.__aenter__()

    session = ClientSession(r, w)
    await session.__aenter__()
    await session.initialize()

    tools = await load_mcp_tools(session)
    llm_with_tools = llm.bind_tools(tools)

    prompt = "add 10 and 20"
    hmsg = HumanMessage(content=prompt)

    print(f"Agent->Prompting Model :{prompt}")
    tc = llm_with_tools.invoke([hmsg])

    print(f"Agent->Got response from Model")

    for t in tc.tool_calls:
        tname = t['name']
        targs = t['args']
        print(f"Agent->Invoking tool :'{tname}' with args :{targs}")

        result = await session.call_tool(name=tname, arguments=targs)
        print(f"Agent->Got Results :{result.content[0].text}")

    await session.__aexit__(None, None, None)
    await client_ctx.__aexit__(None, None, None)
    
if __name__ == "__main__":
    asyncio.run(main())

