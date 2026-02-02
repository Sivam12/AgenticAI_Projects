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
    print('ORCHESTRATOR: init_orchestrator')
    v_ReviewAgentState["git_agent_data"]=None
    return v_ReviewAgentState

async def read_pr_details_from_git(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: read_pr_details_from_git')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    git_return_value= await git_read_agent.ainvoke({"pr_details": v_ReviewAgentState['pr_details']})
    v_ReviewAgentState["git_agent_data"]=git_return_value
    print(f'ORCHESTRATOR: {git_return_value}') 
    return v_ReviewAgentState


def llm_review_code(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: llm_review_code')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    llm_review_agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})

def raise_jira_tickets(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: raise_jira_tickets')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    Jira_Agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})


def write_review_comments_to_git(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: write_review_comments_to_git')

def build_orchestrator():

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

    graph = workflow.compile()

    save_graph_as_png(graph, __file__)

    return graph

# -------------------------
# Main
# -------------------------
async def main():
    graph = build_orchestrator()

    pr_url = 'https://github.com/Sivam12/issue-tracker/pull/1'
    response = await graph.ainvoke({"pr_details": pr_url})
    print(f"ORCHESTRATOR: Response :{response}")

if __name__ == "__main__":
    asyncio.run(main())
