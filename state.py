from typing import TypedDict, List

class AgentState(TypedDict):
    user_id: str
    query: str
    response: str
    memory: List[str]
    next_agent: str