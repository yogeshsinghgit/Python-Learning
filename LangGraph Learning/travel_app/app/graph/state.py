from typing import NotRequired, TypedDict


class TravelState(TypedDict):
    """
    Shared state that flows through every node in the graph.
    """
    user_input: str
    destination: NotRequired[str]
    response: NotRequired[str]