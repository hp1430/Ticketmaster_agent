from langchain.tools import tool

from schemas.tool_schema import EventDetailsInput

from ..client import ticketmaster_client

@tool("get_event_detail", args_schema=EventDetailsInput)
async def get_event_details_tool(event_id: str) -> str:
    """
    Get in-depth policies, rules, age restrictions, and purchase limits for a specific event.
    Use this tool ONLY when the user asks specific questions about an event they already found 
    (e.g., 'Can I bring a camera?', 'What are the age limits?', 'How many tickets can I buy?').
    Requires a valid Ticketmaster event ID.
    """

    res = await ticketmaster_client.get_event_details(event_id=event_id)
    return res.model_dump_json()