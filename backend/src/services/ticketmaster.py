import httpx

from configs.server_config import TICKETMASTER_BASE_URL, TICKETMASTER_API_KEY

class TicketmasterService:
    def __init__(self) -> None:
        self.api_key = TICKETMASTER_API_KEY

    async def search_events(
        self,
        keyword: str,
        city: str | None = None,
        country_code: str | None = None,
        size: int = 10
    ):
        params = {
            "apikey": self.api_key,
            "keyword": keyword,
            "size": size,
        }

        if city:
            params["city"] = city

        if country_code:
            params["countryCode"] = country_code

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{TICKETMASTER_BASE_URL}/events.join",
                    params=params
                )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            print(f"API request failed with status code {e.response.status_code}: {e}")
            
        except Exception as e:
            return f"Failed to search event: {e}"