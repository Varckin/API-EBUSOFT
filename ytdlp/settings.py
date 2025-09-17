from pydantic import BaseModel, Field, HttpUrl
from pathlib import Path


class Settings(BaseModel):
    TMP_DIR_YOUTUBE: Path = Field(default=Path("./tmp/youtube"), description="Folder for temporary files.")
    TMP_DIR_INSTAGRAM: Path = Field(default=Path("./tmp/instagram"), description="Folder for temporary files.")
    TMP_DIR_SOUNDCLOUD: Path = Field(default=Path("./tmp/soundcloud"), description="Folder for temporary files.")

    YOUTUBE_COOKIES_FILE: Path = Field(default=Path("./ytdlp/cookies/youtube_cookies.txt").resolve(), description="Youtube cookies")
    INSTAGRAM_COOKIES_FILE: Path = Field(default=Path("./ytdlp/cookies/insta_cookies.txt").resolve(), description="Instagram cookies")

SETTINGS = Settings()

SETTINGS.TMP_DIR_YOUTUBE.mkdir(parents=True, exist_ok=True)
SETTINGS.TMP_DIR_INSTAGRAM.mkdir(parents=True, exist_ok=True)
SETTINGS.TMP_DIR_SOUNDCLOUD.mkdir(parents=True, exist_ok=True)


class DownloadRequest(BaseModel):
    url: HttpUrl
    id: int
