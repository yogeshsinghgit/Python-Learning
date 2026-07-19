from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from loguru import logger

from app.ai.runtime_dependencies.graph_context import GraphContext
from app.graph.prompts import SYSTEM_PROMPT


async def chatbot_node(
    state: MessagesState,
    context: GraphContext
):
    """
    Main chatbot node.
    """

    logger.info("Executing chatbot node.")

    response = await context.llm.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    logger.info("LLM response generated.")

    return {
        "messages": [response]
    }