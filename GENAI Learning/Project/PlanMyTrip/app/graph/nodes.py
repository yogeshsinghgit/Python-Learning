from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from loguru import logger

from app.graph.prompts import SYSTEM_PROMPT


async def chatbot_node(
    state: MessagesState,
    llm,
):
    """
    Main chatbot node.
    """

    logger.info("Executing chatbot node.")

    response = await llm.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    logger.info("LLM response generated.")

    return {
        "messages": [response]
    }