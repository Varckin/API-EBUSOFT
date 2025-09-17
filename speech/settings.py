from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PositiveInt, Field


class PathsSettings(BaseModel):
    """File paths and temporary file limits."""
    TMP_DIR: Path = Field(default=Path("./tmp/speech"), description="Folder for temporary audio files.")
    MAX_TMP_FILES: PositiveInt = Field(default=40, description="File limit in TMP_DIR, after which the folder is cleaned.")


class STTSettings(BaseModel):
    """Speech recognition settings (Whisper)."""
    WHISPER_MODEL: Literal["tiny", "base", "small", "medium", "large"] = "small"
    AUDIO_FRAME_RATE: PositiveInt = Field(default=16000, description="Sample rate for input audio normalization.")
    AUDIO_CHANNELS: Literal[1, 2] = Field(default=1, description="Number of channels for input audio normalization.")


class TTSSettings(BaseModel):
    """Speech synthesis settings."""
    DEFAULT_LANG: str = Field(default="ru", description="Default TTS language (e.g., 'en', 'ru').")
    OUTPUT_FORMAT: Literal["ogg", "mp3", "wav"] = Field(default="ogg", description="TTS output file format.")
    OGG_CODEC: str = Field(default="libopus", description="Codec for OGG format, if 'ogg' is selected.")


class SpeechSettings(BaseModel):
    """Root configuration for the speech module."""
    PATHS: PathsSettings = PathsSettings()
    STT: STTSettings = STTSettings()
    TTS: TTSSettings = TTSSettings()


SETTINGS = SpeechSettings()

TMP_DIR: Path = SETTINGS.PATHS.TMP_DIR
MAX_TMP_FILES: int = SETTINGS.PATHS.MAX_TMP_FILES

WHISPER_MODEL: str = SETTINGS.STT.WHISPER_MODEL
AUDIO_FRAME_RATE: int = SETTINGS.STT.AUDIO_FRAME_RATE
AUDIO_CHANNELS: int = SETTINGS.STT.AUDIO_CHANNELS

TTS_DEFAULT_LANG: str = SETTINGS.TTS.DEFAULT_LANG
TTS_OUTPUT_FORMAT: str = SETTINGS.TTS.OUTPUT_FORMAT
TTS_OGG_CODEC: str = SETTINGS.TTS.OGG_CODEC

TMP_DIR.mkdir(parents=True, exist_ok=True)
