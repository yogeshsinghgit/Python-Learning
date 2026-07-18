from loguru import logger

from app.ai.travel_agent import TravelAgent


class ChatService:

    def __init__(
        self,
        travel_agent: TravelAgent,
    ):
        self._travel_agent = travel_agent

    async def chat(
        self,
        thread_id: str,
        message: str,
    ) -> str:

        logger.info(
            f"Processing chat request. Thread: {thread_id}"
        )

        response = await self._travel_agent.chat(
            thread_id=thread_id,
            message=message,
        )

        logger.success(
            f"Chat completed. Thread: {thread_id}"
        )

        return response