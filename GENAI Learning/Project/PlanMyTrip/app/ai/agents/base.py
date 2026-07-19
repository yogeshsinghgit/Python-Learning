from abc import ABC, abstractmethod
from typing import Any

from langgraph.graph.state import CompiledStateGraph


class BaseAgent(ABC):
    """
    Base class for all LangGraph agents.
    """

    def __init__(self, checkpointer: Any) -> None:
        builder = self.build_graph()
        self._graph: CompiledStateGraph = builder.compile(
            checkpointer=checkpointer,
        )

    @abstractmethod
    def _build_graph(self):
        """
        Return a StateGraph builder.
        """

    async def invoke(
        self,
        *,
        input: dict,
        config: dict,
    ) -> dict:

        return await self._graph.ainvoke(
            input=input,
            config=config,
        )

    async def stream(
        self,
        *,
        input: dict,
        config: dict,
    ):
        async for chunk in self._graph.astream(
            input=input,
            config=config,
        ):
            yield chunk

    async def get_state(
        self,
        *,
        config: dict,
    ):
        return await self._graph.aget_state(config)

    async def update_state(
        self,
        *,
        config: dict,
        values: dict,
    ):
        return await self._graph.aupdate_state(
            config,
            values,
        )