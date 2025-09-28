import zipfile
from datetime import datetime
from pathlib import Path
from celery_conf import celery_app
from logger.init_logger import get_logger

from ytdlp.youtube import Youtube
from ytdlp.soundcloud import SoundCloud
from ytdlp.instagram import Instagram

logger = get_logger('ytdlp_celery')

def make_zip(files: list[Path], dir: Path) -> Path:
    if not files:
        return None

    zip_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = dir / zip_filename

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=file.name)
            if file != zip_path:
                file.unlink(missing_ok=True)

    logger.info(f"ZIP created: {zip_filename}")
    return zip_path

@celery_app.task
def down_youtube(url: str, id: int) -> str:
    yb = Youtube(str(id))
    files = yb.download_audio(url)
    zip_path = make_zip(files, yb.DOWNLOAD_DIR)
    return str(zip_path) if zip_path else ""


@celery_app.task
def down_soundcloud(url: str, id: int) -> str:
    sc = SoundCloud(str(id))
    files = sc.download_audio(url)
    zip_path = make_zip(files, sc.DOWNLOAD_DIR)
    return str(zip_path) if zip_path else ""


@celery_app.task
def down_instagram(url: str, id: int) -> str:
    insta = Instagram(str(id))
    file_path = insta.download(url)
    zip_path = make_zip([file_path], insta.DOWNLOAD_DIR)
    return str(zip_path) if zip_path else ""
