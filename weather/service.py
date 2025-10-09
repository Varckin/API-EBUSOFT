import httpx, json, urllib.parse
import redis.asyncio as redis
from fastapi import HTTPException
from weather.settings import CONFIG
from weather.models import WeatherResponse


redis_client = redis.from_url(
    CONFIG.redis_broker_url,
    encoding="utf-8",
    decode_responses=True
)

async def redis_check_cached(location: str, lang: str | None = None, fmt: str | None = None) -> WeatherResponse:
    """
    Fetch weather from Redis cache if available, otherwise call fetch_weather and store result.
    """
    settings = CONFIG

    lang = lang or settings.default_lang
    fmt = settings.default_format # It was specially done this way, because I decided this way :)
    safe_location = urllib.parse.quote(location)
    
    cache_key = f"weather:{safe_location}:{lang}:{fmt}"
    cached = await redis_client.get(cache_key)
    if cached:
        data = json.loads(cached)
        return WeatherResponse.model_validate(data)
    
    weather = await fetch_weather(location, lang, fmt)

    await redis_client.set(cache_key, weather.model_dump_json(), ex=settings.cache_ttl)

    return weather

async def fetch_weather(location: str, lang: str | None = None, fmt: str | None = None) -> WeatherResponse:
    """Asynchronously receives the weather"""
    settings = CONFIG

    url = f"{settings.wtr_base_url}/{location}?format={fmt}&lang={lang}"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Error during the request ({response.status_code})")

    try:
        json_data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="It is impossible to decode the response")

    current = json_data.get("current_condition", [{}])[0]
    nearest_area = json_data.get("nearest_area", [{}])[0]

    location_name = nearest_area.get("areaName", [{}])[0].get("value", "N/A")

    weather_desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")

    temperature_c = current.get("temp_C", "N/A")
    feels_like_c = current.get("FeelsLikeC", "N/A")
    humidity = current.get("humidity", "N/A")
    wind_speed_kmph = current.get("windspeedKmph", "N/A")

    return WeatherResponse(
        location=location_name,
        temperature_c=temperature_c,
        feels_like_c=feels_like_c,
        weather_desc=weather_desc,
        humidity=humidity,
        wind_speed_kmph=wind_speed_kmph,
    )
