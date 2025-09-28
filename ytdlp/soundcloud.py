from yt_dlp import YoutubeDL
from pathlib import Path
from ytdlp.settings import SETTINGS
from logger.init_logger import get_logger

logger = get_logger('soundcloud')


class SoundCloud:
    def __init__(self, id: str):
        self.DOWNLOAD_DIR = SETTINGS.TMP_DIR_SOUNDCLOUD / f'{id}'
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def download_audio(self, url: str) -> list[Path]:
        """Download audio from the given SoundCloud URL and return a list of downloaded file paths."""
        before_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))

        ydl_opts = {
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
            logger.warning(f"SoundCloud - Error loading: {e}")
            return []

        after_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
        new_files = list(after_files - before_files)

        if not new_files:
            logger.warning("SoundCloud - Could not find new files after upload.")
        else:
            logger.info("SoundCloud - Download music done!")

        return new_files
