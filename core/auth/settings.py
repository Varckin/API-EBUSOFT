from pydantic import BaseModel
from typing import List
from os import getenv

class Settings(BaseModel):
    TOKEN_TTL_MINUTES: int = 21600
    ADMIN_MASTER_TOKEN: str = getenv('ADMIN_MASTER_TOKEN')
    WHITELIST_PATHS: List[str] = [
        "/",
        "/health",
        "/sollaire",
        "/favicon.ico",
        "/docs",
        "/openapi.json",
        "/admin/health",
        "/admin/add-token",
        "/admin/remove-token",
        "/admin/list-tokens"
    ]


CONFIG = Settings()
