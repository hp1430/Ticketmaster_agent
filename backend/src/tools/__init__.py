from tools.get_event_details import get_event_details_tool
from tools.search_events import search_events_tool
from tools.search_venues_tool import search_venues_tool
from tools.get_venue_details_tool import get_venue_details_tool


ALL_TOOLS = [
    get_event_details_tool,
    search_events_tool,
    search_venues_tool,
    get_venue_details_tool
]

def tool_catalog() -> list[dict[str, str]]:
    """Name + Description of the tools"""
    return [
        {   
            "name": tool.name,
            "description": tool.description
        }
        for tool in ALL_TOOLS
    ]