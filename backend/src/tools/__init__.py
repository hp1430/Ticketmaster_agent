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

def tool_catalog() -> list[dict]:
    """Return the tool metadata and JSON schemas used by the system prompt."""
    catalog = []
    for tool in ALL_TOOLS:
        schema = getattr(tool, "args_schema", None)
        schema_builder = getattr(schema, "model_json_schema", None)
        parameters = schema_builder() if callable(schema_builder) else schema or {}
        catalog.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": parameters,
        })
    return catalog