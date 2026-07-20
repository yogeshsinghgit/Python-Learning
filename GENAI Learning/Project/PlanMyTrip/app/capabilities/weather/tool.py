from typing import Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.capabilities.weather.client import WeatherClient


class WeatherToolInput(BaseModel):
    location: str = Field(
        description="City or destination to check the weather for, e.g. 'Goa'."
    )


class WeatherToolOutput(BaseModel):
    location: str
    temperature_celsius: float
    windspeed_kmh: float
    weather_description: str


class WeatherTool(BaseTool):
    """
    Class-based tool adapting WeatherClient to LangChain's tool
    interface. The client is injected at construction time (DI) —
    this class holds no vendor knowledge and no business logic.
    """

    name: str = "weather_lookup"
    description: str = (
        "Get the current weather for a city or destination. Use this "
        "when the user asks about weather, temperature, or conditions "
        "for a specific place."
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    client: WeatherClient

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError("WeatherTool only supports async execution.")

    async def _arun(self, location: str) -> str:
        result = await self.client.get_weather(location)

        output = WeatherToolOutput(
            location=result.location,
            temperature_celsius=result.temperature_celsius,
            windspeed_kmh=result.windspeed_kmh,
            weather_description=result.weather_description,
        )

        return output.model_dump_json()
