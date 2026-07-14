from typing import NotRequired, TypedDict, Annotated
from graph.reducers import append_lists


class TravelState(TypedDict):
    user_input: str

    intent: NotRequired[str]
    destination: NotRequired[str]

    hotels: NotRequired[list[str]]
    attractions: NotRequired[list[str]]
    # to test reducer
    # places : NotRequired[list[str]]
    # apply reducer
    # places: Annotated[list[str], append_lists]
    # "Whenever multiple nodes update places in the same execution step, don't throw an error. Instead, call append_lists()."

    response: NotRequired[str]