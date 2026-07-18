from loguru import logger

from app.graph.builder import build_graph


class TravelAgent:

    def __init__(
        self,
        llm,
        checkpointer,
    ):
        logger.info("Compiling LangGraph.")

        builder = build_graph(llm)

        self.graph = builder.compile(
            checkpointer=checkpointer,
        )

        logger.success("Travel Agent Ready.")

    async def chat(
        self,
        thread_id: str,
        message: str,
    ) -> str:

        result = await self.graph.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            },
        )

        return result["messages"][-1].content