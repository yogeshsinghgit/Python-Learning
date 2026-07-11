from langgraph.graph import StateGraph, START, END

from graph.state import TravelState
from graph.nodes import (
    parse_user_input,
    generate_greeting
)


builder = StateGraph(TravelState)
# means: "I'm creating a graph whose shared state follows the TravelState schema."
# START and END are special Nodes


# register nodes
builder.add_node(
    "parse_user_input",
    parse_user_input
)

builder.add_node(
    "generate_greeting",
    generate_greeting,
)

# Add Edges
builder.add_edge(
    START,
    "parse_user_input"
)

builder.add_edge(
    "parse_user_input",
    "generate_greeting",
)

builder.add_edge(
    "generate_greeting",
    END,
)

graph = builder.compile()