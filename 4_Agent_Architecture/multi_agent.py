from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from state import AgentState
from tools import ToolRegistry

class MultiAgentSystem:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.registry = ToolRegistry()

    def supervisor(self, state: AgentState) -> dict:
        """Supervisor router deciding next step or synthesis execution."""
        if state["current_step"] >= len(state.get("plan", [])):
            return {"next_step": "synthesize"}
            
        current_objective = state["plan"][state["current_step"]]
        system_prompt = (
            "Evaluate the current objective. "
            "Route to: 'research_worker' (for web or doc search) or 'analyst_worker' (for database metric lookups)."
        )
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Objective: {current_objective}")
        ])
        
        content = response.content.lower()
        if "research" in content:
            next_step = "research_worker"
        else:
            next_step = "analyst_worker"
            
        return {"next_step": next_step}

    def research_worker(self, state: AgentState) -> dict:
        """Worker agent executing research tasks using semantic web search."""
        objective = state["plan"][state["current_step"]]
        tool_output = self.registry.route_tool("web_search", objective)
        return {
            "context": [tool_output],
            "current_step": state["current_step"] + 1,
            "messages": [HumanMessage(content=f"Research complete: {tool_output}")]
        }

    def analyst_worker(self, state: AgentState) -> dict:
        """Worker agent executing analytics query tools."""
        objective = state["plan"][state["current_step"]]
        tool_output = self.registry.route_tool("database_query", objective)
        return {
            "context": [tool_output],
            "current_step": state["current_step"] + 1,
            "messages": [HumanMessage(content=f"Analysis complete: {tool_output}")]
        }
