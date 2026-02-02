from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict,Optional,Any
from Git_Read_Agent import git_read_agent
from LLM_Review_Agent import llm_review_agent
from Jira_Agent import Jira_Agent
import asyncio
import json


class ReviewAgentState(TypedDict):
     pr_details: str
     git_agent_data: Optional[Any]

def init_orchestrator(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: init_orchestrator - start')
    print(f'ORCHESTRATOR: init_orchestrator - input state: {v_ReviewAgentState}')
    v_ReviewAgentState["git_agent_data"]=None
    print(f'ORCHESTRATOR: init_orchestrator - output state: {v_ReviewAgentState}')
    print('ORCHESTRATOR: init_orchestrator - end')
    return v_ReviewAgentState

async def read_pr_details_from_git(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: read_pr_details_from_git - start')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    print(f"ORCHESTRATOR: read_pr_details_from_git - pr_details: {v_ReviewAgentState.get('pr_details')}")
    print(f"ORCHESTRATOR: read_pr_details_from_git - calling git_read_agent.ainvoke(...)")
    git_return_value= await git_read_agent.ainvoke({"pr_details": v_ReviewAgentState['pr_details']})
    # print(f"ORCHESTRATOR: read_pr_details_from_git - git_read_agent returned type: {type(git_return_value)}")
    v_ReviewAgentState["git_agent_data"]=git_return_value
    print(f'ORCHESTRATOR: git_agent_data set. value: {git_return_value}')
    # print(f'ORCHESTRATOR: read_pr_details_from_git - output state: {v_ReviewAgentState}')
    # print('ORCHESTRATOR: read_pr_details_from_git - end')
    return v_ReviewAgentState


def llm_review_code(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: llm_review_code - start')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    print(f"ORCHESTRATOR: llm_review_code - pr_details: {v_ReviewAgentState.get('pr_details')}")
    print(f"ORCHESTRATOR: llm_review_code - git_agent_data present: {v_ReviewAgentState.get('git_agent_data') is not None}")
    print("ORCHESTRATOR: llm_review_code - invoking llm_review_agent.invoke(...)")
    llm_review_agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})
    print('ORCHESTRATOR: llm_review_code - end')

def raise_jira_tickets(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: raise_jira_tickets - start')
    print(f'ORCHESTRATOR: v_ReviewAgentState:  {v_ReviewAgentState}')
    print(f"ORCHESTRATOR: raise_jira_tickets - pr_details: {v_ReviewAgentState.get('pr_details')}")
    print("ORCHESTRATOR: raise_jira_tickets - invoking Jira_Agent.invoke(...)")
    Jira_Agent.invoke({"pr_details": v_ReviewAgentState['pr_details']})
    print('ORCHESTRATOR: raise_jira_tickets - end')


def write_review_comments_to_git(v_ReviewAgentState: ReviewAgentState):
    print('ORCHESTRATOR: write_review_comments_to_git - start')
    print(f'ORCHESTRATOR: write_review_comments_to_git - state: {v_ReviewAgentState}')
    print('ORCHESTRATOR: write_review_comments_to_git - end')

def build_orchestrator():
    print("ORCHESTRATOR: build_orchestrator - start")

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

    print("ORCHESTRATOR: build_orchestrator - compiling workflow")
    graph = workflow.compile()
    print("ORCHESTRATOR: build_orchestrator - compile complete")

    print(f"ORCHESTRATOR: build_orchestrator - saving graph png using file: {__file__}")
    save_graph_as_png(graph, __file__)
    print("ORCHESTRATOR: build_orchestrator - graph png saved")

    print("ORCHESTRATOR: build_orchestrator - end")
    return graph

# -------------------------
# Main
# -------------------------
async def main():
    print("ORCHESTRATOR: main - start")
    graph = build_orchestrator()
    print("ORCHESTRATOR: main - orchestrator graph built")

    pr_url = 'https://github.com/Sivam12/issue-tracker/pull/1'
    print(f"ORCHESTRATOR: main - pr_url: {pr_url}")

    print("ORCHESTRATOR: main - invoking graph.ainvoke(...)")
    response = await graph.ainvoke({"pr_details": pr_url})
    print(f"ORCHESTRATOR: Response :{response}")
    print("ORCHESTRATOR: main - end")

if __name__ == "__main__":
    print("ORCHESTRATOR: __main__ - start")
    asyncio.run(main())
    print("ORCHESTRATOR: __main__ - end")
