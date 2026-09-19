from typing import Optional

from langchain.tools import tool

from schemas.tool_schema import SearchEventsInput
from ..client import ticketmaster_client

@tool("search_events", args_schema=SearchEventsInput)
async def search_events_tool(
    keyword: str,
    city: Optional[str] = None,
    country_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    size: int = 10,
    venue_id: Optional[str] = None
) -> str:
    """
    Search for upcoming live events (concerts, sports, festivals, shows etc.).
    Use this tool whenever the user asks broad discovery questions like
    'What shows are in city X?' or 'Find tickets for artist Y'.
    """

    res = await ticketmaster_client.search_events(
        keyword=keyword,
        city=city,
        country_code=country_code,
        start_date=start_date,
        end_date=end_date,
        size=size,
        venue_id=venue_id
    )
    return res.model_dump_json()
