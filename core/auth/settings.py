from pydantic import BaseModel
from typing import List
from os import getenv

class Settings(BaseModel):
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
    TOKEN_TTL_MINUTES: int = 21600
    ADMIN_MASTER_TOKEN: str = getenv('ADMIN_MASTER_TOKEN')
    WHITELIST_PATHS: List[str] = [
        "/",
        "/docs",
        "/openapi.json",
        "/admin/health",
        "/admin/add-token",
        "/admin/remove-token",
        "/admin/list-tokens"
    ]


CONFIG = Settings()
