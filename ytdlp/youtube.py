from yt_dlp import YoutubeDL
from pathlib import Path
from logger.init_logger import get_logger
from ytdlp.settings import SETTINGS

logger = get_logger('youtube')


class Youtube:
    def __init__(self, id: str):
        self.DOWNLOAD_DIR = SETTINGS.TMP_DIR_YOUTUBE / f'{id}'
        self.YOUTUBE_COOKIES_FILE = SETTINGS.YOUTUBE_COOKIES_FILE
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def download_audio(self, url: str) -> list[Path]:
        before_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))

        ydl_opts = {
            'cookiefile': str(self.YOUTUBE_COOKIES_FILE),
            "format": "bestaudio/best",
            "outtmpl": str(self.DOWNLOAD_DIR / "%(artist,NA)s - %(track,title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "320",
                },
                {"key": "FFmpegMetadata"}
            ],
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "noplaylist": False,
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.warning(f"Youtube - Error loading: {e}")
            return []

        after_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
        new_files = list(after_files - before_files)

        if not new_files:
            logger.warning("Youtube - Could not find new files after upload.")
        else:
            logger.info("Youtube - Download music done!")

        return new_files
