import httpx

from app.capabilities.weather.exceptions import WeatherProviderError
from app.capabilities.weather.provider import WeatherProvider
from app.capabilities.weather.schemas import WeatherQuery, WeatherResult

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather codes -> human-readable description. Subset covering
# the common cases; see https://open-meteo.com/en/docs for the rest.
_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    95: "Thunderstorm",
}


class OpenMeteoWeatherProvider(WeatherProvider):
    """
    Adapter over the free Open-Meteo API. No API key required.
    https://open-meteo.com/
    """

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(timeout=10.0)

    async def get_current_weather(self, query: WeatherQuery) -> WeatherResult:
        location = await self._geocode(query.location)
        forecast = await self._get_forecast(
            location["latitude"],
            location["longitude"],
        )

        current = forecast["current_weather"]

        return WeatherResult(
            location=location["name"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            temperature_celsius=current["temperature"],
            windspeed_kmh=current["windspeed"],
            weather_description=_WEATHER_CODES.get(
                current["weathercode"], "Unknown"
            ),
            observed_at=current["time"],
        )

    async def _geocode(self, location: str) -> dict:
        response = await self._client.get(
            GEOCODING_URL,
            params={"name": location, "count": 1},
        )
        response.raise_for_status()

        results = response.json().get("results")

        if not results:
            raise WeatherProviderError(
                f"No location found for '{location}'."
            )

        return results[0]

    async def _get_forecast(self, latitude: float, longitude: float) -> dict:
        response = await self._client.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
            },
        )
        response.raise_for_status()

        return response.json()
