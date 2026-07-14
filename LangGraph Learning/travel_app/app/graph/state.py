from typing import NotRequired, TypedDict


class TravelState(TypedDict):
    user_input: str

    intent: NotRequired[str]
    destination: NotRequired[str]

    hotels: NotRequired[list[str]]
    attractions: NotRequired[list[str]]

    response: NotRequired[str]