from pydantic import BaseModel, Field


class WeatherQuery(BaseModel):
    """Input to any WeatherProvider. Deliberately vendor-agnostic."""

    location: str = Field(
        description="City or place name, e.g. 'Goa' or 'Paris'."
    )


class WeatherResult(BaseModel):
    """
    Output from any WeatherProvider.

    Every adapter (Open-Meteo, WeatherAPI, whatever comes next) must
    map its vendor-specific response into this shape. Nothing above
    the provider layer ever sees vendor-specific fields.
    """

    location: str
    latitude: float
    longitude: float
    temperature_celsius: float
    windspeed_kmh: float
    weather_description: str
    observed_at: str
