from langgraph.graph import MessagesState

from graph.chatbot import llm_with_tools


def chatbot(state: MessagesState) -> dict:
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }