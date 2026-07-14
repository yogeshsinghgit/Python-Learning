from loguru import logger
from langgraph.types import Command

from graph.constants import FIND_HOTELS, FIND_ATTRACTIONS, GENERATE_GREETING
from graph.state import TravelState
from tools.travel_tools import search_hotels, search_attractions


# def parse_user_input(state: TravelState) -> dict:
#     logger.info("Executing parse_user_input")

#     user_input = state["user_input"]

#     if "trip" in user_input.lower():
#         destination = user_input.split()[-1]

#         return {
#             "intent": "travel",
#             "destination": destination.title(),
#         }

#     return {
#         "intent": "greeting",
#     }

def parse_user_input(
    state: TravelState,
) -> Command:
    logger.info("Executing parse_user_input")

    user_input = state["user_input"]

    if "trip" in user_input.lower():
        destination = user_input.split()[-1].title()

        return Command(
            update={
                "intent": "travel",
                "destination": destination,
            },
            goto=[
                FIND_HOTELS,
                FIND_ATTRACTIONS,
            ],
        )

    return Command(
        update={
            "intent": "greeting",
        },
        goto=GENERATE_GREETING,
    )

def generate_greeting(state: TravelState) -> dict:
    logger.info("Executing generate_greeting")

    return {
        "response": "Hi there!!!"
    }



def find_hotels(state: TravelState) -> dict:
    hotels = search_hotels.invoke(
        {
            "destination": state["destination"],
        }
    )

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
    # return {
    #     "places": attractions,
    # }



def build_response(state: TravelState) -> dict:
    logger.info("Executing build_response")

    destination = state["destination"]

    hotels = state["hotels"]

    attractions = state["attractions"]
    # places = state["places"]

    response = f"Trip Plan\n\n Hotels {hotels} \n\n Attractions {attractions}"

    # for place in places:
    #     response += f"- {place}\n"

    return {
        "response": response,
    }
    