import httpx

from configs.server_config import TICKETMASTER_BASE_URL, TICKETMASTER_API_KEY
from schemas.error import ErrorResponse
from schemas.event import Event, EventDetailsResponse, EventSearchResponse

class TicketmasterService:
    def __init__(self) -> None:
        self.api_key = TICKETMASTER_API_KEY

    async def search_events(
        self,
        keyword: str,
        city: str | None = None,
        country_code: str | None = None,
        size: int = 10,
        start_date: str | None = None,
        end_date: str | None = None
    ) -> EventSearchResponse | ErrorResponse :
        params = {
            "apikey": self.api_key,
            "keyword": keyword,
            "size": size,
        }

        if city:
            params["city"] = city

        if country_code:
            params["countryCode"] = country_code

        if start_date:
            params["startDateTime"] = start_date

        if end_date:
            params["endDateTime"] = end_date

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{TICKETMASTER_BASE_URL}/events.json",
                    params=params
                )

            response.raise_for_status()

            data = response.json()
            raw_events = data.get("_embedded", {}).get("events", [])
            events = []

            for event in raw_events:
                dates = event.get("dates", {}).get("start", {})
                venues = event.get("_embedded", {}).get("venues", [])
                venue = venues[0] if venues else {}

                events.append(
                    Event(
                        id = event.get("id"),
                        name = event.get("name"),
                        date = dates.get("localDate"),
                        time = dates.get("localTime"),
                        venue = venue.get("name"),
                        city = venue.get("city", {}).get("name", ""),
                        url = event.get("url")
                    )
                )

            total = data.get("page", {}).get("totalElements", len(events))

            return EventSearchResponse(
                events=events,
                total=total
            )

        except httpx.HTTPStatusError as e:
            return ErrorResponse(
                success=False,
                error=str(e),
                message="Failed to search event"
            )

        except Exception as e:
            return ErrorResponse(
                success=False,
                error=str(e),
                message="Failed to search event"
            )

    async def get_event_details(self, event_id: str) -> EventDetailsResponse | ErrorResponse :
        params={
            "apikey": self.api_key
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{TICKETMASTER_BASE_URL}/events/{event_id}.json",
                    params=params
                )

            response.raise_for_status()

            event = response.json()
            dates = event.get("dates", {}).get("start", {})
            venues = event.get("_embedded", {}).get("venues", [])
            venue_name = venues[0].get("name") if venues else None
            venue_id = venues[0].get("id") if venues else None

            return EventDetailsResponse(
                id=event.get("id"),
                name=event.get("name"),
                url=event.get("url"),
                date=dates.get("localDate"),
                time=dates.get("localTime"),
                timezone=event.get("dates", {}).get("timezone"),
                venue_name=venue_name,
                venue_id=venue_id,
                promoter=event.get("promoter", {}).get("name"),
                please_note=event.get("pleaseNote"),
                ticket_limit_info=event.get("ticketLimit", {}).get("info")
            )

        except httpx.HTTPStatusError as e:
            return ErrorResponse(
                success=False,
                error=str(e),
                message=f"Failed to fetch event details with status code {e.response.status_code}"
            )
        
        except Exception as e:
            return ErrorResponse(
                success=False,
                error=str(e),
                message="Failed to fetch event details"
            )


    async def search_venues(
            self,
            keyword: str,
            country_code: str | None = None,
            size: int = 10
        ):
            params = {
                "apikey": self.api_key,
                "keyword": keyword,
                "size": size,
            }
    
            if country_code:
                params["countryCode"] = country_code
    
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{TICKETMASTER_BASE_URL}/venues.json",
                        params=params
                    )
    
                response.raise_for_status()
    
                return response.json()
    
            except httpx.HTTPStatusError as e:
                print(f"API request failed with status code {e.response.status_code}: {e}")
    
            except Exception as e:
                return f"Failed to search event: {e}"


    async def get_venue_details(self, venue_id: str):
            params={
                "apikey": self.api_key
            }
    
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{TICKETMASTER_BASE_URL}/venues/{venue_id}.json",
                        params=params
                    )
    
                response.raise_for_status()
    
                return response.json()
    
            except httpx.HTTPStatusError as e:
                print(f"API request failed with status code {e.response.status_code}: {e}")
            
            except Exception as e:
                return f"Failed to search event: {e}"