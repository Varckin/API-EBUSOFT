from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PositiveInt, Field


class PathsSettings(BaseModel):
    """File paths and temporary file limits."""
    TMP_DIR: Path = Field(default=Path("./tmp/speech"), description="Folder for temporary audio files.")
    STT_MODEL_DIR: Path = Field(default=Path("./speech/stt_model"), description="Folder for STT model.")
    MAX_TMP_FILES: PositiveInt = Field(default=40, description="File limit in TMP_DIR, after which the folder is cleaned.")
    MAX_FILE_SIZE_MB: PositiveInt = Field(default=15, description="Maximum upload size for audio files in megabytes.")


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

SETTINGS.PATHS.TMP_DIR.mkdir(parents=True, exist_ok=True)
SETTINGS.PATHS.STT_MODEL_DIR.mkdir(parents=True, exist_ok=True)
