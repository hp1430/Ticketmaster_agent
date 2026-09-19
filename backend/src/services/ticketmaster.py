import httpx

from configs.server_config import TICKETMASTER_BASE_URL, TICKETMASTER_API_KEY
from schemas.error import ErrorResponse
from schemas.event import Event, EventDetailsResponse, EventSearchResponse
from schemas.venue import BoxOfficeDetails, Venue, VenueDetailResponse, VenueSearchResponse

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
        end_date: str | None = None,
        venue_id: str | None = None
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

        if venue_id:
            params["venueId"] = venue_id

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
        ) -> VenueSearchResponse | ErrorResponse:
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
    
                data = response.json()
                raw_venues = data.get("_embedded", {}).get("venues", [])
                venues = []

                for raw_venue in raw_venues:
                    venues.append(
                        Venue(
                            id = raw_venue.get("id"),
                            name=raw_venue.get("name"),
                            city=raw_venue.get("city", {}).get("name"),
                            state=raw_venue.get("state", {}).get("name"),
                            country=raw_venue.get("country", {}).get("name"),
                            address=raw_venue.get("address", {}).get("line1"),
                            postal_code=raw_venue.get("postalCode"),
                            url=raw_venue.get("url")
                        )
                    )
                total = data.get("page", {}).get("totalElements", len(venues))

                return VenueSearchResponse(
                    venues=venues,
                    total=total
                )
    
            except httpx.HTTPStatusError as e:
                return ErrorResponse(
                success=False,
                error=str(e),
                message=f"Failed to search venues with status code {e.response.status_code}"
            )
    
            except Exception as e:
                return ErrorResponse(
                success=False,
                error=str(e),
                message="Failed to search venues"
            )


    async def get_venue_details(self, venue_id: str) -> VenueDetailResponse | ErrorResponse:
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
    
                venue = response.json()
                box_office = venue.get("boxOfficeInfo", {})
                general_info = venue.get("generalInfo", {})

                return VenueDetailResponse(
                id=venue.get("id"),
                name=venue.get("name"),
                url=venue.get("url"),
                postal_code=venue.get("postalCode"),
                timezone=venue.get("timezone"),
                city=venue.get("city", {}).get("name"),
                state=venue.get("state", {}).get("name"),
                country=venue.get("country", {}).get("name"),
                address=venue.get("address", {}).get("line1"),
                box_office=BoxOfficeDetails(
                    phone_detail=box_office.get("phoneNumberDetail"),
                    open_hours=box_office.get("openHoursDetail"),
                    accepted_payments=box_office.get("acceptedPaymentDetail"),
                    will_call_detail=box_office.get("willCallDetail")
                ),
                parking_detail=venue.get("parkingDetail"),
                accessible_seating_detail=venue.get("accessibleSeatingDetail"),
                general_rule=general_info.get("generalRule")
            )
    
            except httpx.HTTPStatusError as e:
                return ErrorResponse(
                success=False,
                error=str(e),
                message=f"Failed to fetch venue details with status code {e.response.status_code}"
            )
            
            except Exception as e:
                return ErrorResponse(
                success=False,
                error=str(e),
                message="Failed to fetch venue details"
            )