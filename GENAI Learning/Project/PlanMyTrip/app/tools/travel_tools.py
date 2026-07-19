from langchain_core.tools import tool


@tool
async def hotel_search(
    destination: str,
) -> str:
    return f"Hotels for {destination}"


@tool
async def attraction_search(
    destination: str,
) -> str:
    return f"Attractions for {destination}"


@tool
async def trip_planner(
    destination: str,
    days: int,
) -> str:
    return f"{days}-day itinerary for {destination}"