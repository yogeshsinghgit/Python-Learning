from graph.state import TravelState


# Node 1 - Parse User Input
def parse_user_input(state: TravelState) -> dict:
    """
    Parse the user's request and determine the intent.

    For this learning project:
    - If the input contains the word 'trip', classify it as a travel request.
    - Otherwise, classify it as a greeting.
    """

    user_input = state["user_input"].lower()

    if "trip" in user_input:
        destination = user_input.split()[-1]

        return {
            "intent": "travel",
            "destination": destination.title(),
        }

    return {
        "intent": "greeting"
    }


def generate_travel_plan(state: TravelState) -> dict:
    """
    Generate a simple travel response.
    """

    destination = state["destination"]

    return {
        "response": f"I'll create a wonderful travel itinerary for your trip to {destination}!"
    }

# Node 2 - Generate Greeting
def generate_greeting(state: TravelState)-> dict:
    """
    Generate a greeting using the extracted destination.
    """
    return {
        "response": f"Hi there!!!"
    }