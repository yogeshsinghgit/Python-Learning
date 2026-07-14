from loguru import logger

from graph.state import TravelState


def parse_user_input(state: TravelState) -> dict:
    logger.info("Executing parse_user_input")

    user_input = state["user_input"]

    if "trip" in user_input.lower():
        destination = user_input.split()[-1]

        return {
            "intent": "travel",
            "destination": destination.title(),
        }

    return {
        "intent": "greeting",
    }


def generate_greeting(state: TravelState) -> dict:
    logger.info("Executing generate_greeting")

    return {
        "response": "Hi there!!!"
    }



def find_hotels(state: TravelState) -> dict:
    logger.info("Executing find_hotels")

    destination = state["destination"]

    hotels = [
        f"{destination} Grand Hotel",
        f"{destination} Central Hotel",
        f"{destination} Palace Hotel",
    ]

    logger.success(f"Found {len(hotels)} hotels")

    return {
        "hotels": hotels,
    }


def find_attractions(state: TravelState) -> dict:
    logger.info("Executing find_attractions")

    destination = state["destination"]

    attractions = [
        f"{destination} Castle",
        f"{destination} National Museum",
        f"{destination} City Park",
    ]

    logger.success(f"Found {len(attractions)} attractions")

    return {
        "attractions": attractions,
    }


def build_response(state: TravelState) -> dict:
    logger.info("Executing build_response")

    destination = state["destination"]

    hotels = state["hotels"]

    attractions = state["attractions"]

    response = f"""
Trip Plan for {destination}

Hotels:
- {hotels[0]}
- {hotels[1]}
- {hotels[2]}

Attractions:
- {attractions[0]}
- {attractions[1]}
- {attractions[2]}
""".strip()

    logger.success("Travel response created")

    return {
        "response": response,
    }