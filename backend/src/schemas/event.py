from dataclasses import dataclass
from typing import Optional

@dataclass
class Event():
    id: str
    name: str
    date: str | None = None
    time: str | None = None
    venue: str | None = None
    city: str | None = None
    url: str | None = None

@dataclass
class EventSearchResponse():
    events: list[Event]
    total: int

@dataclass
class EventDetailsResponse():
    id: str
    name: str
    url: str
    date: Optional[str] = None
    time: Optional[str] = None
    timezone: Optional[str] = None
    venue_name: Optional[str] = None
    venue_id: Optional[int] = None
    promoter: Optional[str] = None
    please_note: Optional[str] = None
    ticket_limit_info: Optional[str] = None