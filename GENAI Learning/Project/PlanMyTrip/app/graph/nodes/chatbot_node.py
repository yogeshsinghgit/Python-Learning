from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from loguru import logger

from app.ai.runtime_dependencies.graph_context import GraphContext
from app.graph.state import GraphState
from app.graph.prompts import SYSTEM_PROMPT
from app.tools import TOOL_REGISTRY


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

    planner_decision = state["planner_decision"]

    planner_context = f"""
        Planner Intent: {planner_decision.intent.value}
        Allowed Tools:
        {", ".join(tool.name for tool in allowed_tools) or "none"}
        Only use the above tools if required.
        If no tool is required, answer normally.
        """.strip()

    system_message = SystemMessage(
        content=f"{SYSTEM_PROMPT}\n\n{planner_context}"
    )

    allowed_tools = [
        TOOL_REGISTRY[name]
        for name in planner_decision.tool_names
        if name in TOOL_REGISTRY
    ]

    llm = context.llm
    if planner_decision.should_use_tools and allowed_tools:
        llm = llm.bind_tools(allowed_tools)

    response = await llm.ainvoke(
        [
            system_message,
            *state["messages"],
        ]
    )


    logger.success("Chatbot response generated.")

    return {
        "messages": [response]
    }