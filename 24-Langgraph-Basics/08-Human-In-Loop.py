import random
from langgraph.graph import StateGraph, START, END
from langgraph.pregel.retry import RetryPolicy
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


# Node 1: Auto random + retry
def is_prime(state):
    for i in range(1, 4):  # auto retry 3 times
        num = random.randint(-10, 5)
        try:
            state["is_prime"] = check_prime(num)
            print(f"[Auto Attempt {i}] Checked number {num} → Prime? {state['is_prime']}")
            return state
        except ValueError as e:
            print(f"[Auto Attempt {i}] Failed with number {num} → {e}")

    # after 3 failures, let router send us to human
    state["is_prime"] = None
    return state

# Node 2: Human-in-the-middle fallback
def human_review(state):
    print("⚠️ Automatic retries exhausted. Switching to HUMAN mode...")
    for i in range(1, 4):  # up to 3 human attempts
        try:
            num = int(input(f"[Human Attempt {i}] Enter a positive number to check prime: "))
            state["is_prime"] = check_prime(num)
            print(f"[Human Attempt {i}] Checked number {num} → Prime? {state['is_prime']}")
            return state
        except Exception as e:
            print(f"[Human Attempt {i}] Failed → {e}")
    raise ValueError("❌ Human retries also failed. Aborting.")


def main():
    # Build LangGraph
    graph = StateGraph(dict)

    # Add nodes
    graph.add_node(
        "is_prime",
        is_prime,
        retry=RetryPolicy(
            retry_on=(ValueError,),
            max_attempts=3
        )
    )
    graph.add_node("human_review", human_review)

    # Edges
    graph.add_edge(START, "is_prime")

    # Instead of add_error_handler → use conditional edge
    def router(state):
        # If automatic retries happened 3 times but still no result, go to human
        if state.get("is_prime") is None:
            return "human_review"
        return END

    graph.add_conditional_edges("is_prime", router, {"human_review": "human_review", END: END})
    graph.add_edge("human_review", END)

    # Compile
    app = graph.compile()
    save_graph_as_png(app, __file__)

    # Run
    for i in range(5):
        print("\n🔹 Run", i+1)
        try:
            result = app.invoke({})
            print("✅ Final Result:", result)
        except Exception as e:
            print("❌ Workflow failed:", e)

if __name__ == "__main__":
    main()
