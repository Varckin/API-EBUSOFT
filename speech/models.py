from pydantic import BaseModel, Field
from speech.settings import SETTINGS

class STTResponse(BaseModel):
    text: str = Field(..., description="Recognized speech text.")
    language: str = Field(..., description="Detected language code (e.g. 'en', 'ru').")


class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize into speech.")
    lang: str = Field(
        default=SETTINGS.TTS.DEFAULT_LANG,
        description="Language code for synthesis (e.g., 'en', 'ru')."
    )
