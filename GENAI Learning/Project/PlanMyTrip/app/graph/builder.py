from functools import partial

from langgraph.graph import END, START, StateGraph

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

    builder.add_edge(
        START,
        "planner",
    )

    builder.add_edge(
        "planner",
        "chatbot",
    )

    builder.add_edge(
        "chatbot",
        END,
    )

    return builder