from pydantic import BaseModel

class Event(BaseModel):
    id: str
    name: str
    date: str | None = None
    time: str | None = None
    venue: str | None = None
    city: str | None = None
    url: str | None = None

class EventSearchResponse(BaseModel):
    events: list[Event]
    total: int