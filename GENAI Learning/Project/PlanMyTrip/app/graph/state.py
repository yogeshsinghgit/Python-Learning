from langgraph.graph import MessagesState

from app.ai.planner.models import PlannerDecision


class GraphState(MessagesState):
    """
    Shared state flowing through the LangGraph execution.

    MessagesState already provides:
        - messages

    We extend it with application-specific state required by
    our workflow.
    """

    planner_decision: PlannerDecision | None = None