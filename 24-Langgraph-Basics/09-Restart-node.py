import random
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


def is_prime(state):
    # Initialize counters
    state["attempts"] = state.get("attempts", 0)

    for i in range(1, 4):  # 3 tries in this "round"
        num = random.randint(-10, 5)
        try:
            state["is_prime"] = check_prime(num)
            print(f"[Round {state['attempts']//3 + 1}, Attempt {i}] Checked number {num} → Prime? {state['is_prime']}")
            return state
        except ValueError as e:
            print(f"[Round {state['attempts']//3 + 1}, Attempt {i}] Failed with number {num} → {e}")
            state["attempts"] += 1

    # If 3 attempts failed → clear result and route back to is_prime again
    state["is_prime"] = None
    return state


def router(state):
    # If success → end, else restart is_prime
    if state.get("is_prime") is None:
        print("🔄 Restarting is_prime after 3 failed attempts...")
        return "is_prime"
    return END


# Build LangGraph
graph = StateGraph(dict)
graph.add_node("is_prime", is_prime)
graph.set_entry_point("is_prime")

graph.add_conditional_edges("is_prime", router, {"is_prime": "is_prime", END: END})

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
