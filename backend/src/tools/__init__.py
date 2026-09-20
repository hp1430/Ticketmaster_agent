from tools import get_event_details, get_venue_details_tool, search_events, search_venues_tool


ALL_TOOLS = [
    get_event_details,
    search_events,
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