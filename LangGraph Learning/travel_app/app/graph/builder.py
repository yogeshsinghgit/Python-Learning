from langgraph.graph import StateGraph, START, END

from graph.state import TravelState
from graph.edges import route_request
from graph.nodes import (
    parse_user_input,
    generate_greeting,
    generate_travel_plan
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

builder.add_node(
    "generate_travel_plan",
    generate_travel_plan,
)

# Add Edges
builder.add_edge(
    START,
    "parse_user_input"
    
)

# builder.add_edge(
#     "parse_user_input",
#     "generate_greeting",
# )

builder.add_conditional_edges(
    "parse_user_input", # source node
    route_request, # router function
    # path map 
    {   # The left side is the value returned by the router.
        # The right side is the node registered in the graph.
        "generate_travel_plan": "generate_travel_plan",
        "generate_greeting": "generate_greeting",
    },

)

# Finally connect both nodes to END.
builder.add_edge(
    "generate_greeting",
    END,
)

builder.add_edge(
    "generate_travel_plan",
    END,
)
graph = builder.compile()