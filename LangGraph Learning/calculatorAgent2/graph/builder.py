from langgraph.graph import StateGraph, END

from states.calculator_state import CalculatorState
from nodes.parse_node import parse_node
from nodes.planner_node import planner_node
from nodes.add_node import add_node
from nodes.multiply_node import multiply_node
from nodes.answer_node import answer_node
from graph.routing import route_after_planner


def build_graph():
    builder = StateGraph(CalculatorState)

    builder.add_node("parse", parse_node)
    builder.add_node("planner", planner_node)
    builder.add_node("add", add_node)
    builder.add_node("multiply", multiply_node)
    builder.add_node("answer", answer_node)

    builder.set_entry_point("parse")

    builder.add_edge("parse", "planner")

    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "add": "add",
            "answer": "answer"
        }
    )

    builder.add_edge("add", "multiply")
    builder.add_edge("multiply", "answer")
    builder.add_edge("answer", END)

    return builder.compile()