from functools import partial

from langgraph.graph import END, START, MessagesState, StateGraph

from app.graph.nodes import chatbot_node


def build_graph(llm):

    builder = StateGraph(MessagesState)

    builder.add_node(
        "chatbot",
        partial(
            chatbot_node,
            llm=llm,
        ),
    )

    builder.add_edge(
        START,
        "chatbot",
    )

    builder.add_edge(
        "chatbot",
        END,
    )

    return builder