from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse

from speech.STT import STT
from speech.TTS import TTS
from speech.settings import SETTINGS
from speech.models import STTResponse, TTSRequest

router = APIRouter(prefix="/speech", tags=["speech"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the speech module."""
    return "ok"


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(file: UploadFile = File(...)):
    """
    Convert speech to text.
    Accepts an audio file, returns recognized text and language.
    """
    stt = STT()
    contents = await file.read()

    if len(contents) > SETTINGS.PATHS.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max allowed size is {SETTINGS.PATHS.MAX_FILE_SIZE_MB} MB."
        )

    source_path = SETTINGS.PATHS.TMP_DIR / file.filename
    destination_path = SETTINGS.PATHS.TMP_DIR / f"stt_{file.filename}.wav"

    with open(source_path, "wb") as f:
        f.write(contents)

    text, lang = stt.convert_voice_to_text(source_path, destination_path)
    return STTResponse(text=text, language=lang)


@router.post("/tts")
async def text_to_speech(request: TTSRequest = Body(...)):
    """
    Convert text to speech.
    Accepts text and language (e.g., 'en', 'ru'), returns .ogg/.mp3/.wav (based on settings).
    """
    tts = TTS()
    output_path = tts.convert_text_to_voice(request.text, request.lang)
    return FileResponse(
        path=output_path,
        media_type=f"audio/{output_path.suffix.lstrip('.')}",
        filename=output_path.name,
    )
