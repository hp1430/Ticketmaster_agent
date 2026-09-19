from typing import List, Optional

from pydantic import BaseModel

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

class BoxOfficeDetails(BaseModel):
    phone_detail: Optional[str] = None
    open_hours: Optional[str] = None
    accepted_payments: Optional[str] = None
    will_call_detail: Optional[str] = None

class VenueDetailResponse(BaseModel):
    id: str
    name: str
    url: Optional[str] = None
    postal_code: Optional[str] = None
    timezone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    box_office: Optional[BoxOfficeDetails] = None
    parking_detail: Optional[str] = None
    accessible_seating_detail: Optional[str] = None
    general_rule: Optional[str] = None