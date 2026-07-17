from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    confirm_booking,
    prepare_booking,
    wait_for_approval,
)
from graph.state import BookingState

builder = StateGraph(BookingState)

builder.add_node("prepare_booking", prepare_booking)
builder.add_node("wait_for_approval", wait_for_approval)
builder.add_node("confirm_booking", confirm_booking)

builder.add_edge(START, "prepare_booking")
builder.add_edge("prepare_booking", "wait_for_approval")
builder.add_edge("wait_for_approval", "confirm_booking")
builder.add_edge("confirm_booking", END)

memory = InMemorySaver()

graph = builder.compile(
    checkpointer=memory,
)