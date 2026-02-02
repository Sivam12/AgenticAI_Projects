from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict

class JiraAgent(TypedDict):
     Jira_ticket_details: str

def ConnectJira(v_JiraAgent: JiraAgent):
    print('JIRA_AGENT: ConnectJira')

def CreateTickets(v_JiraAgent: JiraAgent):
    print('JIRA_AGENT: CreateTickets')


workflow = StateGraph(JiraAgent)


workflow.add_node("CONNECT_JIRA_NODE", ConnectJira)
workflow.add_node("CREATE_TICKETS_NODE", CreateTickets)

workflow.add_edge(START, "CONNECT_JIRA_NODE")
workflow.add_edge("CONNECT_JIRA_NODE", "CREATE_TICKETS_NODE")
workflow.add_edge("CREATE_TICKETS_NODE", END)

Jira_Agent = workflow.compile()

save_graph_as_png(Jira_Agent, __file__)

if __name__ == "__main__":
    response = Jira_Agent.invoke({"Jira_ticket_details": 'github.com/pr1'})
    print(f"JIRA_AGENT: Response :{response}")
