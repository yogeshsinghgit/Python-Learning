from langchain_core.tools import tool


@tool
def search_hotels(destination: str) -> list[str]:
    """
    Search hotels for a destination.
    """

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

    return [
        f"{destination} Castle",
        f"{destination} National Museum",
        f"{destination} City Park",
    ]