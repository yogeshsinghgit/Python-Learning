from langgraph.graph import StateGraph, END
from states import CalculatorState
from nodes import parse_node, add_node, multiply_node, answer_node

# create graph
builder = StateGraph(CalculatorState)

# add nodes
builder.add_node("parse", parse_node)
builder.add_node("add", add_node)
builder.add_node("multiply", multiply_node)
builder.add_node("answer", answer_node)

# define edges
builder.set_entry_point("parse")

builder.add_edge("parse", "add")
builder.add_edge("add", "multiply")
builder.add_edge("multiply", "answer")
builder.add_edge("answer", END)

# compile graph
graph = builder.compile()

initial_state = CalculatorState(
    user_input="Add 10 and 5 then multiply by 3"
)

result = graph.invoke(initial_state)

print(result)