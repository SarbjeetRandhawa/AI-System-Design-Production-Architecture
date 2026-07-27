from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from planning import PlanningEngine
from multi_agent import MultiAgentSystem

# Initialize components
planner = PlanningEngine()
multi_agent = MultiAgentSystem()

# Define the Synthesize Node
def synthesize_node(state: AgentState) -> dict:
    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    context_str = "\n".join(state.get("context", []))
    query = state["messages"][0].content
    
    prompt = f"Context:\n{context_str}\n\nUser Query: {query}\n\nFormulate a final grounded response:"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_response": response.content}

# Propose Action Node (Requires human verification)
def propose_action_node(state: AgentState) -> dict:
    return {"approved": False}

# Build LangGraph Workflow
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("plan", planner.plan_and_solve)
workflow.add_node("supervisor", multi_agent.supervisor)
workflow.add_node("research_worker", multi_agent.research_worker)
workflow.add_node("analyst_worker", multi_agent.analyst_worker)
workflow.add_node("propose_action", propose_action_node)
workflow.add_node("synthesize", synthesize_node)

# Connect Flow
workflow.set_entry_point("plan")
workflow.add_edge("plan", "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_step"],
    {
        "research_worker": "research_worker",
        "analyst_worker": "analyst_worker",
        "synthesize": "propose_action"
    }
)

workflow.add_edge("research_worker", "supervisor")
workflow.add_edge("analyst_worker", "supervisor")

# HITL Interrupt gate before final synthesis execution
workflow.add_edge("propose_action", "synthesize")
workflow.add_edge("synthesize", END)

memory_checkpointer = MemorySaver()
agent_app = workflow.compile(
    checkpointer=memory_checkpointer,
    interrupt_before=["synthesize"]
)

if __name__ == "__main__":
    print("Modular Agent Architecture Graph compiled successfully.")
