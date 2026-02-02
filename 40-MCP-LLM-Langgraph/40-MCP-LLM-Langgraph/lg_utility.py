# src/37-Multiple-Agents-Orchestrator/lg_utility.py
import os
from langgraph.graph import MessagesState
from langchain_core.runnables.graph_mermaid import MermaidDrawMethod

def save_graph_as_png(graph, filename=None):
    if filename is None:
        filename = os.path.splitext(os.path.basename(__file__))[0]
    
    # png_bytes = graph.get_graph().draw_mermaid_png()
    png_bytes = graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)
    with open(f"{filename}.png", "wb") as f:
        f.write(png_bytes)

# src/35-Orchestrator/utils.py
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pdbwhereami import whocalledme
from termcolor import cprint
import json

def dump_state(state: MessagesState):
    messages = state["messages"]

    for msg in messages:
        msg.pretty_print()
        
def dump_prompt(prompt):
    msg = whocalledme(verbose=False) + ' prompt '
    cprint('{:*^100}'.format(msg), 'white')
    
    for i, msg_obj in enumerate(prompt):
        msg_type = msg_obj.__class__.__name__
        content = msg_obj.content.strip()
        print(f"{i+1:02d}. [{msg_type}]: {content}")
        print(" ")
    
    print(" ")

def dump_response(response):
    msg = whocalledme(verbose=False) + ' response '
    cprint('{:-^100}'.format(msg), 'white')
    print(response.content)
    print(" ")

def dump_final_response(final_output):
    final_dict = dict(final_output)
   
    for i, msg in enumerate(final_dict["messages"], 1):
        print(i, msg)
    
    print(final_dict["messages"][-1])
    print(final_dict["messages"][-1].content)
