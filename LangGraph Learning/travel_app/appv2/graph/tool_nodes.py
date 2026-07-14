from langgraph.prebuilt import ToolNode

from tools.travel_tools import (
    search_attractions,
    search_hotels,
)

tool_node = ToolNode(
    [
        search_hotels,
        search_attractions,
    ]
)