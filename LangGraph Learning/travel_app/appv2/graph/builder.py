from langgraph.graph import (
    END,
    START,
    MessagesState,
    StateGraph,
)
from langgraph.prebuilt import tools_condition

from graph.nodes import chatbot
from graph.tool_nodes import tool_node


builder = StateGraph(MessagesState)

builder.add_node(
    "chatbot",
    chatbot,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_edge(
    START,
    "chatbot",
)

builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

builder.add_edge(
    "tools",
    "chatbot",
)

graph = builder.compile()