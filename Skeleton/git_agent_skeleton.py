# git_agent.py
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END

# -------------------------
# Git Agent State
# -------------------------
class GitAgentState(TypedDict):
    owner: str
    repo: str
    pull_number: int

    connected: bool
    output: Optional[str]

# -------------------------
# Node 1: git_init (sync)
# -------------------------
def git_init(state: GitAgentState) -> GitAgentState:
    print("[GIT] git_init")
    state["connected"] = False
    state["output"] = None
    return state

# -------------------------
# Node 2: git_mcp_connect (async)
# -------------------------
async def git_mcp_connect(state: GitAgentState) -> GitAgentState:
    print("[GIT] git_mcp_connect (dummy async)")
    # pretend async work
    state["connected"] = True
    return state

# -------------------------
# Node 3: git_output_node (sync)
# -------------------------
def git_output_node(state: GitAgentState) -> GitAgentState:
    print("[GIT] git_output_node")
    state["output"] = f"Fetched PR #{state['pull_number']} from {state['owner']}/{state['repo']}"
    return state

# -------------------------
# Build Git Agent Graph
# -------------------------
def build_git_agent():
    graph = StateGraph(GitAgentState)

    graph.add_node("GIT_INIT", git_init)
    graph.add_node("GIT_MCP_CONNECT", git_mcp_connect)
    graph.add_node("GIT_OUTPUT", git_output_node)

    graph.add_edge(START, "GIT_INIT")
    graph.add_edge("GIT_INIT", "GIT_MCP_CONNECT")
    graph.add_edge("GIT_MCP_CONNECT", "GIT_OUTPUT")
    graph.add_edge("GIT_OUTPUT", END)

    return graph.compile()

git_agent_graph = build_git_agent()
