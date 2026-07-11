from graph.state import TravelState


def route_request(state: TravelState) -> str:
    """
    Decide which node should execute next.
    """

    intent = state["intent"]

    if intent == "travel":
        return "generate_travel_plan"

    return "generate_greeting"