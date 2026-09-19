from pydantic import BaseModel
from typing import List, Optional

class Venue(BaseModel):
    id: str
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    url: Optional[str] = None

class VenueSearchResponse(BaseModel):
    venues: List[Venue]
    total: int