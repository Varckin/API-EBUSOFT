from pathlib import Path
from uuid import uuid4
from yt_dlp import YoutubeDL
from logger.init_logger import get_logger
from ytdlp.settings import SETTINGS

logger = get_logger('insta')


class Instagram:
    def __init__(self, id: str):
        self.DOWNLOAD_DIR = SETTINGS.TMP_DIR_INSTAGRAM / f'{id}'
        self.INSTAGRAM_COOKIES_FILE = SETTINGS.INSTAGRAM_COOKIES_FILE
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def is_instagram_url(url: str) -> bool:
        """Check if the given URL is a valid Instagram post or reel URL."""
        return any(sub in url for sub in ["instagram.com/reels/", "instagram.com/reel/", "instagram.com/p/", "instagram.com/tv/"])

    def download(self, url: str) -> Path | None:
        """Download the Instagram video from the given URL and return the local file path, or None if failed."""
        if not self.is_instagram_url(url):
            logger.info(f"Instagram - Not valid url: {url}")
            return None

        output_path = self.DOWNLOAD_DIR / f"{str(uuid4().hex[:8])}.mp4"

        ydl_opts = {
            'cookiefile': str(self.INSTAGRAM_COOKIES_FILE),
            'outtmpl': str(output_path),
            'format': "bestvideo+bestaudio/best",
            'quiet': True,
            'noplaylist': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info("Instagram - Download done!")
            return output_path if output_path.exists() else None
        except Exception as e:
            logger.warning(f"Instagram - {e}")
            return None
