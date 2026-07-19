from functools import partial

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.tools import TRAVEL_TOOLS

from app.graph.nodes.chatbot_node import chatbot_node
from app.graph.nodes.planner_node import planner_node
from app.graph.state import GraphState
from app.ai.runtime_dependencies.graph_context import GraphContext


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
        ToolNode(TRAVEL_TOOLS),
    )


    builder.add_edge(
        START,
        "planner",
    )

    builder.add_edge(
        "planner",
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

    

    return builder