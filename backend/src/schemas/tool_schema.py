from pydantic import BaseModel, Field
from typing import Optional

class SearchEventsInput(BaseModel):
    keyword: str = Field(
        description="The search term for the event, artist, team, or tour (e.g., 'Coldplay', 'Monster Jam', 'Lakers')."
    )
    city: Optional[str] = Field(
        default=None, 
        description="Filter events by city name (e.g., 'Mexico City', 'London', 'New York')."
    )
    country_code: Optional[str] = Field(
        default=None, 
        description="Two-letter country code in ISO-3166 format (e.g., 'MX', 'US', 'GB')."
    )
    start_date: Optional[str] = Field(
        default=None, 
        description="Start date/time in ISO-8601 UTC format (e.g., '2026-10-01T00:00:00Z')."
    )
    end_date: Optional[str] = Field(
        default=None, 
        description="End date/time in ISO-8601 UTC format (e.g., '2026-10-31T23:59:59Z')."
    )
    size: int = Field(
        default=10, 
        description="Number of results to return (max 20 recommended for context efficiency)."
    )
    venue_id: Optional[str] = Field(
        default=None,
        description="The unique Ticketmaster ID of the venue (e.g., 'KovZpZA77t6A')."
    )

class EventDetailsInput(BaseModel):
    event_id: str = Field(
        description="The unique Ticketmaster ID of the event (e.g., '1AfZk34Gkdve0pI')."
    )

class SearchVenuesInput(BaseModel):
    keyword: str = Field(
        description="Name of the venue, arena, stadium, or theater (e.g., 'Palacio de los Deportes', 'Madison Square Garden')."
    )
    country_code: Optional[str] = Field(
        default=None, 
        description="Two-letter country code in ISO-3166 format (e.g., 'MX', 'US')."
    )
    size: int = Field(default=5, description="Number of venue matches to return.")

class VenueDetailsInput(BaseModel):
    venue_id: str = Field(
        description="The unique Ticketmaster ID of the venue (e.g., 'KovZpZA77t6A')."
    )