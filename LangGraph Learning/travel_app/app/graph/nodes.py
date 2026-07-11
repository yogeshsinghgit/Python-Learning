from graph.state import TravelState


# Node 1 - Parse User Input
def parse_user_input(state: TravelState) -> dict:
    """
    Extract the travel destination from the user's input.

    For this learning project, we'll simply assume the last word
    in the sentence is the destination.
    """
    user_input = state["user_input"]

    destination = user_input.split()[-1]

    return {
        "destination": destination
    }

# Node 2 - Generate Greeting
def generate_greeting(state: TravelState)-> dict:
    """
    Generate a greeting using the extracted destination.
    """
    destination = state["destination"]

    return {
        "response": f"Great! Let's plan your trip to {destination}"
    }