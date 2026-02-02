# orchestrator.py
import asyncio
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from git_agent_skeleton import git_agent_graph

# -------------------------
# Orchestrator State
# -------------------------
class OrchestratorState(TypedDict):
    owner: str
    repo: str
    pull_number: int

    git_result: Optional[str]

# -------------------------
# Node 1: orchestrator_init (sync)
# -------------------------
def orchestrator_init(state: OrchestratorState) -> OrchestratorState:
    print("[ORCH] orchestrator_init")
    state["git_result"] = None
    return state

# -------------------------
# Node 2: invoke_git_agent_node (async)
# -------------------------
async def invoke_git_agent_node(state: OrchestratorState) -> OrchestratorState:
    print("[ORCH] invoke_git_agent_node")

    git_state = await git_agent_graph.ainvoke({
        "owner": state["owner"],
        "repo": state["repo"],
        "pull_number": state["pull_number"],
    })

    state["git_result"] = git_state["output"]
    return state

# -------------------------
# Node 3: orchestrator_output_node (sync)
# -------------------------
def orchestrator_output_node(state: OrchestratorState) -> OrchestratorState:
    print("[ORCH] orchestrator_output_node")
    print("FINAL RESULT:", state["git_result"])
    return state

# -------------------------
# Build Orchestrator Graph
# -------------------------
def build_orchestrator():
    graph = StateGraph(OrchestratorState)

    graph.add_node("ORCH_INIT", orchestrator_init)
    graph.add_node("INVOKE_GIT", invoke_git_agent_node)
    graph.add_node("ORCH_OUTPUT", orchestrator_output_node)

    graph.add_edge(START, "ORCH_INIT")
    graph.add_edge("ORCH_INIT", "INVOKE_GIT")
    graph.add_edge("INVOKE_GIT", "ORCH_OUTPUT")
    graph.add_edge("ORCH_OUTPUT", END)

    return graph.compile()

# -------------------------
# Main
# -------------------------
async def main():
    graph = build_orchestrator()

    await graph.ainvoke({
        "owner": "promptlyaig",
        "repo": "issue-tracker",
        "pull_number": 1
    })

if __name__ == "__main__":
    asyncio.run(main())
