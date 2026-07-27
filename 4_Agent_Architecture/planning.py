from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from state import AgentState

class PlanningEngine:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

    def plan_and_solve(self, state: AgentState) -> dict:
        """Decomposes the high-level objective into sequential plan steps."""
        query = state["messages"][0].content
        system_prompt = (
            "Decompose the user query into a sequence of maximum 3 discrete steps. "
            "Return only the steps separated by newlines."
        )
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Decompose this task: {query}")
        ])
        steps = [step.strip() for step in response.content.split("\n") if step.strip()]
        return {"plan": steps, "current_step": 0}

    def reflexion_critique(self, state: AgentState) -> dict:
        """Evaluates previous draft response against the retrieved context to verify factual alignment."""
        draft = state.get("final_response", "")
        context_str = "\n".join(state.get("context", []))
        
        prompt = (
            f"Context:\n{context_str}\n\nDraft Answer:\n{draft}\n\n"
            "Analyze the draft for factual grounding. "
            "Respond with 'PASSED' if grounded, or list missing facts/corrections."
        )
        response = self.llm.invoke([HumanMessage(content=prompt)])
        is_passed = "PASSED" in response.content.upper()
        return {"iterations": state.get("iterations", 0) + 1, "approved": is_passed}
