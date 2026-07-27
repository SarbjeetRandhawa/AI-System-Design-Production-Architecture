import operator
from typing import Annotated, Any, Dict, List, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """The central short-term memory state tracking agent trajectories."""
    messages: Annotated[List[BaseMessage], operator.add]
    plan: List[str]
    current_step: int
    context: List[str]
    tools_selected: List[str]
    final_response: str
    approved: bool
    iterations: int
    next_step: str

class BlackboardState(TypedDict):
    """Blackboard architecture for shared multi-agent state space."""
    shared_hypotheses: Dict[str, Any]
    agent_outputs: Dict[str, Any]
    lock: bool
