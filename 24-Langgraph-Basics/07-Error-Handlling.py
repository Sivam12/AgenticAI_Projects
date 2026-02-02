import random
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy
from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png


def check_prime(n: int) -> bool:
    if n <= 1:
        raise ValueError(f"Invalid number {n}, must be > 0")
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Node 2: Is Prime
def is_prime(state):
    state["attempts"] = state.get("attempts", 0) + 1
    num = random.randint(-10, 10)
    try:
        state["is_prime"] = check_prime(num)
        print(f"[Attempt {state['attempts']}] Checked number {num} → Prime? {state['is_prime']}")
        return state
    except ValueError as e:
        print(f"[Attempt {state['attempts']}] Failed with number {num} → {e}")
        raise

def main():
    # Build LangGraph
    graph = StateGraph(dict)

    # Add is_prime with RetryPolicy (in case ValueError occurs)
    # graph.add_node("is_prime", is_prime)
    graph.add_node("is_prime", is_prime,
        retry=RetryPolicy(
            retry_on=(ValueError,),  # retry only if number <= 0
            max_attempts=3           # try up to 3 times
        )
    )

    graph.add_edge(START, "is_prime")
    graph.add_edge("is_prime", END)

    # Compile
    app = graph.compile()
    save_graph_as_png(app, __file__)

    for i in range(5):
        print("\nRun", i+1)
        try:
            result = app.invoke({})
            print("Final Result:", result)
        except Exception as e:
            print("Failed after retries:", e)

if __name__ == "__main__":
    main()
