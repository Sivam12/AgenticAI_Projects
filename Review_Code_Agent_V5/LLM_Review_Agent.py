from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict

class LLMReviewAgent(TypedDict):
     llm_review_details: str

def AnalyzeCode(v_LLMReviewAgent: LLMReviewAgent):
    print('\n[LLM] AnalyzeCode')
    print('  └─ ✓ Code analyzed')

def GenerateReview(v_LLMReviewAgent: LLMReviewAgent):
    print('\n[LLM] GenerateReview')
    print('  └─ ✓ Review generated')

def IdentifyBugs(v_LLMReviewAgent: LLMReviewAgent):
    print('\n[LLM] IdentifyBugs')
    print('  └─ ✓ Bugs identified')

def SuggestTests(v_LLMReviewAgent: LLMReviewAgent):
    print('\n[LLM] SuggestTests')
    print('  └─ ✓ Tests suggested')


print("\n[LLM] Initializing llm_review_agent...")

workflow = StateGraph(LLMReviewAgent)


workflow.add_node("ANALYZE_CODE_NODE", AnalyzeCode)
workflow.add_node("GENERATE_REVIEW_NODE", GenerateReview)
workflow.add_node("IDENTIFY_BUGS_NODE", IdentifyBugs)
workflow.add_node("SUGGEST_TESTS_NODE", SuggestTests)

workflow.add_edge(START, "ANALYZE_CODE_NODE")
workflow.add_edge("ANALYZE_CODE_NODE", "GENERATE_REVIEW_NODE")
workflow.add_edge("GENERATE_REVIEW_NODE", "IDENTIFY_BUGS_NODE")
workflow.add_edge("IDENTIFY_BUGS_NODE", "SUGGEST_TESTS_NODE")
workflow.add_edge("SUGGEST_TESTS_NODE", END)

print("  └─ Compiling LLM workflow...")
llm_review_agent = workflow.compile()

print("  └─ Saving graph visualization...")
save_graph_as_png(llm_review_agent, __file__)
print("  └─ ✓ llm_review_agent ready\n")

if __name__ == "__main__":
    print("\n[LLM] Running as main...")
    response = llm_review_agent.invoke({"llm_review_details": 'github.com/pr1'})
    print(f"\n[LLM] Response: {response}")