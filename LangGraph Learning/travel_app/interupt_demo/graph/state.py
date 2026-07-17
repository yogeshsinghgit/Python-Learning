from typing import TypedDict


class BookingState(TypedDict):
    destination: str
    hotel_name: str
    approved: bool