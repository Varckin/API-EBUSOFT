from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

from speech.STT import STT
from speech.TTS import TTS
from speech.settings import TMP_DIR, TTS_DEFAULT_LANG

router = APIRouter(prefix="/speech", tags=["speech"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the speech module."""
    return "ok"


@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Convert speech to text.
    Accepts an audio file, returns recognized text and language.
    """
    stt = STT()

    source_path = TMP_DIR / file.filename
    destination_path = TMP_DIR / f"stt_{file.filename}.wav"

    with open(source_path, "wb") as f:
        f.write(await file.read())

    text, lang = stt.convert_voice_to_text(source_path, destination_path)
    return JSONResponse(content={"text": text, "language": lang})


@router.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    lang: str = Form(TTS_DEFAULT_LANG),
):
    """
    Convert text to speech.
    Accepts text and language (e.g., 'en', 'ru'), returns .ogg/.mp3/.wav (based on settings).
    """
    tts = TTS()
    output_path = tts.convert_text_to_voice(text, lang)
    return FileResponse(
        path=output_path,
        media_type=f"audio/{output_path.suffix.lstrip('.')}",
        filename=output_path.name,
    )
