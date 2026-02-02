from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict,Optional,Any
from Git_Read_Agent import git_read_agent
from LLM_Review_Agent import llm_review_agent
from Jira_Agent import Jira_Agent
import asyncio


class ReviewAgentState(TypedDict):
     pr_details: str
     git_agent_data: Optional[Any]

def init_orchestrator(v_ReviewAgentState: ReviewAgentState):
    print('\n[ORCH] init_orchestrator')
    v_ReviewAgentState["git_agent_data"]=None
    print('  └─ ✓ State initialized')
    return v_ReviewAgentState

async def read_pr_details_from_git(v_ReviewAgentState: ReviewAgentState):
    print('\n[ORCH] read_pr_details_from_git')
    print(f"  └─ PR: {v_ReviewAgentState['pr_details']}")
    print(f"  └─ Calling git_read_agent...")
    
    git_return_value = await git_read_agent.ainvoke({"pr_details": v_ReviewAgentState['pr_details']})
    v_ReviewAgentState["git_agent_data"] = git_return_value
    
    print(f'  └─ ✓ Git data received')
    return v_ReviewAgentState


def llm_review_code(v_ReviewAgentState: ReviewAgentState):
    print('\n[ORCH] llm_review_code')
    print(f"  └─ Has git data: {v_ReviewAgentState.get('git_agent_data') is not None}")
    print("  └─ Calling llm_review_agent...")
    llm_review_agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})
    print('  └─ ✓ Review complete')

def raise_jira_tickets(v_ReviewAgentState: ReviewAgentState):
    print('\n[ORCH] raise_jira_tickets')
    print("  └─ Calling Jira_Agent...")
    Jira_Agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})
    print('  └─ ✓ Jira tickets created')


def write_review_comments_to_git(v_ReviewAgentState: ReviewAgentState):
    print('\n[ORCH] write_review_comments_to_git')
    print('  └─ ✓ Comments written to Git')

def build_orchestrator():
    print("\n[ORCH] build_orchestrator")

    workflow = StateGraph(ReviewAgentState)

    workflow.add_node("ORCHESTRATOR_INIT", init_orchestrator)
    workflow.add_node("GIT_READ_NODE", read_pr_details_from_git)
    workflow.add_node("LLM_AGENT_NODE", llm_review_code)
    workflow.add_node("RAISE_JIRA_TICKETS_NODE", raise_jira_tickets)
    workflow.add_node("GIT_WRITE_REVIEW_COMMNETS_NODE", write_review_comments_to_git)

    workflow.add_edge(START, "ORCHESTRATOR_INIT")
    workflow.add_edge("ORCHESTRATOR_INIT", "GIT_READ_NODE")
    workflow.add_edge("GIT_READ_NODE", "LLM_AGENT_NODE")
    workflow.add_edge("LLM_AGENT_NODE", "RAISE_JIRA_TICKETS_NODE")
    workflow.add_edge("RAISE_JIRA_TICKETS_NODE", "GIT_WRITE_REVIEW_COMMNETS_NODE")
    workflow.add_edge("GIT_WRITE_REVIEW_COMMNETS_NODE", END)

    print("  └─ Compiling orchestrator workflow...")
    graph = workflow.compile()

    print(f"  └─ Saving graph visualization...")
    save_graph_as_png(graph, __file__)
    print("  └─ ✓ Orchestrator ready")

    return graph

# -------------------------
# Main
# -------------------------
async def main():
    print("\n" + "="*60)
    print("[ORCH] Starting Review Agent")
    print("="*60)
    
    graph = build_orchestrator()

    pr_url = 'https://github.com/Sivam12/issue-tracker/pull/1'
    print(f"\n[ORCH] Processing PR: {pr_url}")
    print("-"*60)
    
    response = await graph.ainvoke({"pr_details": pr_url})
    
    print("\n" + "="*60)
    print(f"[ORCH] Response: {response}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n[ORCH] Running Review Agent...")
    asyncio.run(main())
    print("[ORCH] ✓ Complete\n")