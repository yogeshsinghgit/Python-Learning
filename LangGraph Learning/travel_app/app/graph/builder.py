from langgraph.graph import START, END, StateGraph

from graph.constants import (
    BUILD_RESPONSE,
    FIND_ATTRACTIONS,
    FIND_HOTELS,
    GENERATE_GREETING,
    PARSE_USER_INPUT,
)
from graph.nodes import (
    build_response,
    find_attractions,
    find_hotels,
    generate_greeting,
    parse_user_input,
)
from graph.routing import route_request
from graph.state import TravelState


builder = StateGraph(TravelState)

builder.add_node(PARSE_USER_INPUT, parse_user_input)
builder.add_node(GENERATE_GREETING, generate_greeting)
builder.add_node(FIND_HOTELS, find_hotels)
builder.add_node(FIND_ATTRACTIONS, find_attractions)
builder.add_node(BUILD_RESPONSE, build_response)

builder.add_edge(START, PARSE_USER_INPUT)

builder.add_conditional_edges(
    PARSE_USER_INPUT,
    route_request,
)

builder.add_edge(
    [FIND_HOTELS, FIND_ATTRACTIONS],
    BUILD_RESPONSE,
)

builder.add_edge(GENERATE_GREETING, END)
builder.add_edge(BUILD_RESPONSE, END)

graph = builder.compile()