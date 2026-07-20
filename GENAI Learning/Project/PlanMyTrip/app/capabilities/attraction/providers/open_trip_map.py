import httpx

from app.core.config import settings
from app.capabilities.attraction.exceptions import AttractionProviderError
from app.capabilities.attraction.provider import AttractionProvider
from app.capabilities.attraction.schemas import Attraction, AttractionQuery, AttractionResult

GEONAME_URL = "https://api.opentripmap.com/0.1/en/places/geoname"
RADIUS_URL = "https://api.opentripmap.com/0.1/en/places/radius"

DEFAULT_RADIUS_METERS = 10_000


class OpenTripMapAttractionProvider(AttractionProvider):
    """
    Adapter over the OpenTripMap API (free tier, requires a free API
    key from https://dev.opentripmap.org/product).
    """

    def __init__(
        self,
        api_key: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._client = client or httpx.AsyncClient(timeout=10.0)

    async def search_attractions(self, query: AttractionQuery) -> AttractionResult:
        coordinates = await self._geocode(query.location)

        attractions = await self._search_radius(
            latitude=coordinates["lat"],
            longitude=coordinates["lon"],
            limit=query.limit,
        )

        return AttractionResult(
            location=coordinates.get("name", query.location),
            attractions=attractions,
        )

    async def _geocode(self, location: str) -> dict:
        response = await self._client.get(
            GEONAME_URL,
            params={"name": location, "apikey": self._api_key},
        )
        response.raise_for_status()
        data = response.json()

        if "lat" not in data or "lon" not in data:
            raise AttractionProviderError(
                f"No location found for '{location}'."
            )

        return data

    async def _search_radius(
        self,
        latitude: float,
        longitude: float,
        limit: int,
    ) -> list[Attraction]:
        response = await self._client.get(
            RADIUS_URL,
            params={
                "radius": DEFAULT_RADIUS_METERS,
                "lat": latitude,
                "lon": longitude,
                "limit": limit,
                "rate": 2,
                "format": "json",
                "apikey": self._api_key,
            },
        )
        response.raise_for_status()

        return [
            Attraction(
                name=item.get("name") or "Unnamed attraction",
                category=(item.get("kinds") or "").split(",")[0] or "general",
                distance_meters=item.get("dist"),
            )
            for item in response.json()
            if item.get("name")
        ]
