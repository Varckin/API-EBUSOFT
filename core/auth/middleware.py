from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from core.base.base import AsyncSessionLocal
from core.auth.models import Token
from datetime import datetime, timezone
from core.auth.settings import CONFIG
from starlette.middleware.base import BaseHTTPMiddleware
from logger.init_logger import get_logger

logger = get_logger('Token_auth_middleware')

class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.whitelist_paths = CONFIG.WHITELIST_PATHS

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path in self.whitelist_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning(f"Missing or invalid Authorization header: path={request.url.path}")
            return JSONResponse({"detail": "Missing or invalid token"}, status_code=401)

        token_value = auth_header.split(" ")[1]

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Token).where(Token.token == token_value))
            token_obj = result.scalars().first()

            if not token_obj:
                logger.warning(f"Invalid token attempt: token={token_value}, path={request.url.path}")
                return JSONResponse({"detail": "Invalid token"}, status_code=401)
            if token_obj.revoked:
                logger.warning(f"Revoked token attempt: token={token_value}, path={request.url.path}, revoked={token_obj.revoked}")
                return JSONResponse({"detail": "Token revoked"}, status_code=401)
            if token_obj.expires_at < datetime.now(timezone.utc):
                logger.warning(f"Expired token attempt: token={token_value}, role={token_obj.role}, expires_at={token_obj.expires_at}, path={request.url.path}")
                return JSONResponse({"detail": "Token expired"}, status_code=401)

            logger.info(f"Token validated: token={token_obj.token}, role={token_obj.role}, expires_at={token_obj.expires_at}, path={request.url.path}")
            request.state.token_info = {"token": token_obj.token, "role": token_obj.role}

        return await call_next(request)
