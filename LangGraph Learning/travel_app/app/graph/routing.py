from typing import Sequence

from graph.constants import (
    FIND_ATTRACTIONS,
    FIND_HOTELS,
    GENERATE_GREETING,
)
from graph.state import TravelState


def route_request(state: TravelState) -> str | Sequence[str]:
    if state["intent"] == "travel":
        return [
            FIND_HOTELS,
            FIND_ATTRACTIONS,
        ]

    return GENERATE_GREETING