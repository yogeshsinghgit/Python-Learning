from langchain_core.messages import AIMessage, HumanMessage
from loguru import logger

from app.graph.state import GraphState


async def clarify_node(
    state: GraphState,
) -> dict:
    """
    Directly asks the user for clarification on the destination.
    Bypasses LLM execution to save latency and token usage.
    """
    logger.info("Clarify node started.")

    user_msg = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            user_msg = str(msg.content).lower()
            break

    if "india" in user_msg:
        content = (
            "Here are some popular destinations in India:\n"
            "- Goa\n"
            "- Kerala\n"
            "- Himachal Pradesh\n\n"
            "Please pick one of these or specify any other destination to plan your trip!"
        )
    elif any(
        word in user_msg
        for word in ["foreign", "international", "abroad", "outside"]
    ):
        content = (
            "Here are some popular international destinations:\n"
            "- Paris\n"
            "- Switzerland\n"
            "- Tokyo\n\n"
            "Please pick one of these or specify any other destination to plan your trip!"
        )
    else:
        content = (
            "I would love to help you plan a trip! Would you like to "
            "explore destinations in India or a foreign country?"
        )

    logger.success("Clarify node response generated.")

    return {
        "messages": [AIMessage(content=content)],
    }
