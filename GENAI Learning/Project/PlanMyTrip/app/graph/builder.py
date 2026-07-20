from functools import partial

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.graph.nodes.chatbot_node import chatbot_node
from app.graph.nodes.planner_node import planner_node
from app.graph.nodes.clarify_node import clarify_node
from app.graph.state import GraphState
from app.ai.runtime_dependencies.graph_context import GraphContext


def route_planner(state: GraphState) -> str:
    """
    Routes the graph from the planner node.
    If the intent is TRIP_PLANNING and the destination is not specified,
    routes to clarify node; otherwise routes to chatbot.
    """
    decision_dict = state.get("planner_decision")
    if not decision_dict:
        return "chatbot"

    intent = decision_dict.get("intent")
    extracted_entities = decision_dict.get("extracted_entities") or {}

    if intent == "trip_planning":
        destination = extracted_entities.get("destination")
        if not destination or not str(destination).strip():
            return "clarify"

    return "chatbot"


def build_graph(context: GraphContext):

    builder = StateGraph(GraphState)

    builder.add_node(
        "planner",
        partial(
            planner_node,
            context=context,
        ),
    )

    builder.add_node(
        "chatbot",
        partial(
            chatbot_node,
            context=context,
        ),
    )

    builder.add_node(
        "tools",
        ToolNode(context.tools),
    )

    builder.add_node(
        "clarify",
        clarify_node,
    )

    builder.add_edge(
        START,
        "planner",
    )

    builder.add_conditional_edges(
        "planner",
        route_planner,
        {
            "clarify": "clarify",
            "chatbot": "chatbot",
        },
    )

    builder.add_edge(
        "clarify",
        END,
    )

    builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )

    builder.add_edge(
        "tools",
        "chatbot",
    )

    return builder