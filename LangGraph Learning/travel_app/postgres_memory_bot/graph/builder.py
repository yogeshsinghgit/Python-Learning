from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, MessagesState, StateGraph

from core.database import get_connection
from graph.nodes import chatbot

builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

connection = get_connection()

checkpointer = PostgresSaver(connection)

checkpointer.setup() # <-Run once to create the tables

graph = builder.compile(
    checkpointer=checkpointer,
)