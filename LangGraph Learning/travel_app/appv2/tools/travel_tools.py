from langchain_core.tools import tool
from loguru import logger


@tool
def search_hotels(destination: str) -> list[str]:
    """
    Search hotels for a destination.
    """
    logger.info(f"Executing tool: search_hotels({destination})")

    return [
        f"{destination} Grand Hotel",
        f"{destination} Central Hotel",
        f"{destination} Palace Hotel",
    ]


@tool
def search_attractions(destination: str) -> list[str]:
    """
    Search tourist attractions.
    """
    logger.info(f"Executing tool: search_attractions({destination})")

    return [
        f"{destination} Castle",
        f"{destination} National Museum",
        f"{destination} City Park",
    ]