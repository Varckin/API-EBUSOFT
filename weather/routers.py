from fastapi import APIRouter, Depends
from weather.models import WeatherQuery, WeatherResponse
from weather.service import redis_check_cached


router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the weather module."""
    return "ok"


@router.get("", response_model=WeatherResponse)
async def get_weather(query: WeatherQuery = Depends()):
    """
    Returns the current weather by city name.
    """
    return await redis_check_cached(
        location=query.location,
        lang=query.lang,
        fmt=query.format
    )
