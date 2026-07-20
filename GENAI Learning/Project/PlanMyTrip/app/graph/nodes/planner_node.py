from loguru import logger
from langchain_core.messages import HumanMessage

from app.graph.state import GraphState
from app.ai.planner.models import PlannerRequest
from app.ai.runtime_dependencies.graph_context import GraphContext


async def planner_node(
    state: GraphState,
    context: GraphContext,
) -> dict:
    """
    Executes the planning stage of the graph.

    Responsibilities:
        - Read the latest user message.
        - Build a PlannerRequest.
        - Invoke the PlannerService.
        - Store the PlannerDecision in graph state.

    This node does NOT:
        - Route the graph.
        - Execute tools.
        - Generate the final response.
    """

    logger.info("Planner node started.")

    human_messages = [
        message
        for message in state["messages"]
        if isinstance(message, HumanMessage)
    ]

    if not human_messages:
        raise ValueError(
            "Planner node expected at least one HumanMessage."
        )

    latest_message = human_messages[-1]

    request = PlannerRequest(
        query=latest_message.content,
        history=state["messages"][:-1],
    )

    decision = await context.planner.plan(request)

    logger.success(
        "Planner node completed successfully. intent={}",
        decision.intent,
    )

    return {
        "planner_decision": decision.model_dump(mode="json"),
    }