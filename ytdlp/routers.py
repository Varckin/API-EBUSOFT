from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from ytdlp.celery_tasks import down_youtube, down_instagram, down_soundcloud
from celery.result import AsyncResult
from celery_conf import celery_app
from ytdlp.settings import DownloadRequest

router = APIRouter(prefix="/ytdlp", tags=["ytdlp"])


@router.post("/youtube")
async def youtube_rout(data: DownloadRequest):
    task = down_youtube.delay(data.url, data.id)
    return {"status": "started", "task_id": task.id}

@router.post("/soundcloud")
async def soundcloud_rout(data: DownloadRequest):
    task = down_soundcloud.delay(data.url, data.id)
    return {"status": "started", "task_id": task.id}

@router.post("/instagram")
async def instagram_rout(data: DownloadRequest):
    task = down_instagram.delay(data.url, data.id)
    return {"status": "started", "task_id": task.id}

@router.get("/status/{task_id}")
async def youtube_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "SUCCESS":
        file_path = task_result.result
        if file_path:
            return {"status": "done", "zip_url": f"/download/{str(file_path)}"}
        return {"status": "done", "zip_url": None}
    return {"status": task_result.state}

@router.get("/download/{filename}")
async def youtube_download_zip(filename: str):
    zip_path = Path(filename)
    if zip_path.exists():
        return FileResponse(zip_path, filename=zip_path.name)
    raise HTTPException(status_code=404, detail="ZIP not found")
