from langgraph.graph import MessagesState

class TravelState(MessagesState):
    itinerary: dict
    budget: int
    destination: str