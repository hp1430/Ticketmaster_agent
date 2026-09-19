from typing import Optional
from langchain.tools import tool
from schemas.tool_schema import SearchVenuesInput

from ..client import ticketmaster_client

@tool("search_venues", args_schema=SearchVenuesInput)
async def search_venues_tool(
    keyword: str, 
    country_code: Optional[str] = None, 
    size: int = 5
) -> str:
    """
    Search for venues, arenas, or stadiums by name.
    Use this when the user mentions a specific venue and wants to look it up directly.
    """
    res = await ticketmaster_client.search_venues(
        keyword=keyword,
        country_code=country_code,
        size=size
    )
    return res.model_dump_json()