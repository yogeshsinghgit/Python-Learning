from langchain_core.tools import tool


@tool
async def hotel_search(destination: str) -> str:
    """Search for hotels in a destination. Currently returns mocked data."""
    return f"Hotels for {destination}"
