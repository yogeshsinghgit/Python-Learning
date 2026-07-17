from pprint import pprint

from loguru import logger
from langgraph.types import Command

from graph.builder import graph

config = {
    "configurable": {
        "thread_id": "booking-demo"
    }
}

logger.info("Starting booking workflow...")

result = graph.invoke(
    {},
    config=config,
)

pprint(result)

if "__interrupt__" in result:
    logger.info("Graph paused.")

    user_input = input("Approve booking (yes/no): ")

    result = graph.invoke(
        Command(
            resume=user_input,
        ),
        config=config,
    )

    logger.success("Graph resumed.")

    pprint(result)