from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from loguru import logger

from app.ai.runtime_dependencies.graph_context import GraphContext
from app.graph.state import GraphState
from app.graph.prompts import SYSTEM_PROMPT


async def chatbot_node(
    state: GraphState,
    context: GraphContext
)-> dict:
    """
    Main chatbot node.

    Responsibilities:
        - Generate the assistant response.
        - Append the response to the graph state.

    This node does NOT:
        - Perform planning.
        - Execute tools.
        - Perform routing.
    """

    logger.info("Chatbot node started.")

    response = await context.llm.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    logger.success("Chatbot response generated.")

    return {
        "messages": [response]
    }