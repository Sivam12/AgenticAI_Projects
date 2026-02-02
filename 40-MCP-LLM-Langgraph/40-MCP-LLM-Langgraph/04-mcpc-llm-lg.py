import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages import AIMessage

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt

from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from functools import partial
from lg_utility import save_graph_as_png

def assistant(state: MessagesState, llm_tools):
    smsg = "You are a helpful assistant tasked with performing arithmetic on a set of inputs."
    sys_msg = SystemMessage(content=smsg)
    response = llm_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

async def create_graph(session):
    MODEL = "gemini-2.0-flash"
    model = ChatVertexAI(model_name=MODEL)
    
    tools = await load_mcp_tools(session)
    model_with_tools = model.bind_tools(tools)

    system_prompt = await load_mcp_prompt(session, "system_prompt")
    print(f"sys_prompt :{system_prompt}")

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", partial(assistant, llm_tools=model_with_tools))
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)    
    builder.add_edge("tools", "assistant")
    graph = builder.compile()

    # save_graph_as_png(graph, __file__)
    
    return graph

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"

    client_ctx = streamablehttp_client(SERVER_URL)
    r, w, _ = await client_ctx.__aenter__()

    session = ClientSession(r, w)
    await session.__aenter__()
    await session.initialize()

    react_graph = await create_graph(session)
    
    prompt = "add 10 and 20"
    hmsg = HumanMessage(content=prompt)
    messages = [hmsg]

    print(f"Agent->Prompting Model :{prompt}")
    response = react_graph.invoke({"messages": messages})

    print(f"Agent->Got response from Model, Tools to invoke")

    tool_invocations = []

    for msg in response["messages"]:
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
            for tool in msg.tool_calls:
                tool_invocations.append(tool)

    for tool in tool_invocations:
        tname = tool['name']
        targs = tool['args']
        print(f"\tAgent->Invoking tool :'{tname}' with args :{targs}")
        result = await session.call_tool(name=tname, arguments=targs)
        print(f"\tAgent->Got Results :{result.content[0].text}")

    await session.__aexit__(None, None, None)
    await client_ctx.__aexit__(None, None, None)
    
if __name__ == "__main__":
    asyncio.run(main())

