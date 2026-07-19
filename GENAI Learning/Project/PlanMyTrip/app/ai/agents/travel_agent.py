from langchain_core.messages import AIMessage

from app.ai.agents.base import BaseAgent
from app.ai.runtime import AgentRuntime
from app.graph.builder import build_graph


class TravelAgent(BaseAgent):

    def __init__(
        self,
        runtime: AgentRuntime,):

        self._runtime = runtime
    
        super().__init__(runtime.checkpointer.client)

    def build_graph(self):
        return _build_graph(
            llm=self._runtime.llm.client,
        )

    async def chat(
        self,
        thread_id: str,
        message: str,
    ) -> str:

        result = await self.invoke(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id,
                }
            },
        )

        last = result["messages"][-1]

        if isinstance(last, AIMessage):
            return last.content

        return str(last)