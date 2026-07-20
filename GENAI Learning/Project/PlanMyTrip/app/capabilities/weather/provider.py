from abc import ABC, abstractmethod

from app.capabilities.weather.schemas import WeatherQuery, WeatherResult


class WeatherProvider(ABC):
    """
    Port: anything that can answer "what's the weather at X"
    implements this. WeatherClient depends only on this interface,
    never on a concrete vendor.
    """

    @abstractmethod
    async def get_current_weather(self, query: WeatherQuery) -> WeatherResult:
        """Return current weather conditions for the given location."""
