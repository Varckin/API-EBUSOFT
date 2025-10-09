from pydantic import BaseModel, Field
from typing import Optional


class WeatherQuery(BaseModel):
    location: str = Field(..., description="City name (example: London)")
    lang: Optional[str] = Field(None, description="Response language (example: ru, en)")
    format: Optional[str] = Field(None, description="Response format (default: j2)")


class WeatherResponse(BaseModel):
    location: str
    temperature_c: str
    feels_like_c: str
    weather_desc: str
    humidity: str
    wind_speed_kmph: str
