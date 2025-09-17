# Упрощаем импорт роутера снаружи:
from .routers import router
from .settings import settings

__all__ = ["router", "settings"]
