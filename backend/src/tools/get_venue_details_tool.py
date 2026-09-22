from langchain.tools import tool
from schemas.tool_schema import VenueDetailsInput

from client import ticketmaster_client

@tool("get_venue_details", args_schema=VenueDetailsInput)
async def get_venue_details_tool(venue_id: str) -> str:
    """
    Retrieve specific venue logistical details including physical address, box office 
    hours, accepted payment methods, and parking information.
    Requires a valid Ticketmaster venue ID.
    """
    res = await ticketmaster_client.get_venue_details(venue_id=venue_id)
    return res.model_dump_json()