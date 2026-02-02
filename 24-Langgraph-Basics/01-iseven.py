from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict

class State(TypedDict):
    value: int

def is_even(state: State):
    print(state["value"])
    if state["value"] % 2 == 0:
        tstr = f"{state['value']} is Even number"
    else:
        tstr = f"{state['value']} is Odd number"
        
    print(tstr)
    return state

def build_graph():
    builder = StateGraph(State)
    
    builder.add_node("EVEN_ODD", is_even)

    builder.add_edge(START, "EVEN_ODD")
    builder.add_edge("EVEN_ODD", END)

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


graph = build_graph()
    

def main():
    response = graph.invoke({"value": 10})
    print(f"Response :{response}")
    print()
    
if __name__ == "__main__":
    main()
