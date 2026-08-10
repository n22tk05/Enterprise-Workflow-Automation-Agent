from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from src.tools import TOOLS_LIST
from src.state.graph_state import AgentState

# 1. Khởi tạo LLM (Sử dụng Groq siêu tốc độ với Llama-3.1)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 2. "Trang bị" danh sách tools cho con AI
llm_with_tools = llm.bind_tools(TOOLS_LIST)

def agent_node(state: AgentState):
    """
    LLM decide whether to call a tool or not
    """
    return {
        'messages': [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful enterprise assistant. You can check leave balances, create leave requests, get profiles, and search company policies."
                    )
                ]
                + state['messages']
            )
        ]
    }

def should_continue(state: AgentState) -> str:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages = state['messages']
    last_message = messages[-1]

    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return 'continue'
    return 'end'

checkpointer = MemorySaver()

action_node = ToolNode(TOOLS_LIST)

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("action", action_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action", # Rẽ vào trạm hành động
        "end": END            # Hoặc đi ra cửa kết thúc
    }
)

workflow.add_edge("action", "agent")

app = workflow.compile(checkpointer=checkpointer)
