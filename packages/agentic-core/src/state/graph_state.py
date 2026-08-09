from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    """
    State schema for angent
    """
    messages: Annotated[list, add_messages]

    is_suspended: bool
    current_user_id: str


