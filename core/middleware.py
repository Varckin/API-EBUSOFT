from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
from core.settings import CONFIG
from logger.init_logger import get_logger


logger = get_logger('rate_limit')


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis_client = redis.from_url(CONFIG.redis_broker_url, decode_responses=True)

    async def dispatch(self, request: Request, call_next):
        ip_header = request.headers.get("X-Forwarded-For")
        ip = ip_header.split(",")[0].strip() if ip_header else request.client.host

        key = f"rate:{ip}"

        current = await self.redis_client.incr(key)
        if current == 1:
            await self.redis_client.expire(key, CONFIG.period_seconds)

        logger.info(f"RateLimit - IP: {ip}, Requests: {current}")

        if current > CONFIG.max_requests:
            logger.warning(f"RateLimit exceeded - IP: {ip}, Requests: {current}")
            raise HTTPException(status_code=429, detail="Too many requests")

        response = await call_next(request)
        return response
