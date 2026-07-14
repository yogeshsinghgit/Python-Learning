from graph.state import TravelState


def route_request(state: TravelState) -> str:
    intent = state["intent"]

    if intent == "travel":
        return "start_travel_workflow"

    return "greeting"