from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph import MessagesState

from graph.nodes import chatbot

builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

memory = InMemorySaver()

graph = builder.compile(
    checkpointer=memory,
)