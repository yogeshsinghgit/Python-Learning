from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from loguru import logger

from app.ai.planner.exceptions import (
    PlannerError,
    PlannerGenerationError,
)
from app.ai.planner.models import PlannerDecision, PlannerRequest
from app.ai.planner.prompts import PlannerPrompts


class PlannerService:
    """
    Generates a structured planning decision for an incoming user query.

    Responsibilities:
        - Build the planner prompt.
        - Invoke the LLM using structured output.
        - Validate the returned decision.
        - Log planner execution.

    This service NEVER:
        - Calls external tools.
        - Updates graph state.
        - Performs routing.
        - Generates the final user response.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        available_tools: list[str] | None = None,
    ) -> None:
        self._prompt = PlannerPrompts.SYSTEM
        self._available_tools = available_tools or []

        self._planner_llm = llm.with_structured_output(
            PlannerDecision
        )

    async def plan(
        self,
        request: PlannerRequest,
    ) -> PlannerDecision:
        """
        Analyse a user query and return a structured planning decision.

        Args:
            request: PlannerRequest containing the query and history.

        Returns:
            PlannerDecision

        Raises:
            PlannerGenerationError:
                Raised when the planner cannot generate a valid decision.
        """

        logger.info("Planner started.")

        logger.debug(
            "Planning query: {}",
            request.query,
        )

        try:
            prompt = self._prompt.invoke(
                {
                    "query": request.query,
                    "history": request.history,
                    "available_tools": ", ".join(self._available_tools) or "none",
                }
            )

            logger.debug("Planner prompt constructed successfully.")

            decision = await self._planner_llm.ainvoke(
                prompt
            )

            logger.success(
                "Planner completed successfully. "
                "intent={} tools={} confidence={}",
                decision.intent,
                decision.tool_names,
                decision.confidence,
            )

            return decision

        except PlannerError:
            raise

        except Exception as exc:
            logger.exception(
                "Planner failed while processing the user query."
            )

            raise PlannerGenerationError(
                "Failed to generate planner decision."
            ) from exc