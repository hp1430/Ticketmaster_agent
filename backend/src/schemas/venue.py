from dataclasses import dataclass

from typing import List, Optional

@dataclass
class Venue():
    id: str
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    url: Optional[str] = None

@dataclass
class VenueSearchResponse():
    venues: List[Venue]
    total: int

@dataclass
class BoxOfficeDetails():
    phone_detail: Optional[str] = None
    open_hours: Optional[str] = None
    accepted_payments: Optional[str] = None
    will_call_detail: Optional[str] = None

@dataclass
class VenueDetailResponse():
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