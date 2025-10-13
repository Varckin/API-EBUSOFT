from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment
import whisper, warnings

from logger.init_logger import get_logger
from speech.settings import SETTINGS


logger = get_logger("STT")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


class STT:
    def __init__(self):
        self.model = whisper.load_model(SETTINGS.STT.WHISPER_MODEL)

    def convert_voice_to_text(self, source_path: Path, destination_path: Path) -> tuple[str, str]:
        """
        Converts input audio file to wav with specified parameters and performs speech recognition.
        Returns (text, language).
        """
        try:
            sound = AudioSegment.from_file(source_path)
            sound = sound.set_channels(SETTINGS.STT.AUDIO_CHANNELS).set_frame_rate(SETTINGS.STT.AUDIO_FRAME_RATE)
            sound.export(destination_path, format="wav")

            result = self.model.transcribe(str(destination_path))

            self._check_tmp_files()
            return result["text"], result["language"]
        except Exception as e:
            logger.error(e)
            return "", ""

    def _check_tmp_files(self) -> None:
        files = [f for f in SETTINGS.PATHS.TMP_DIR.iterdir() if f.is_file()]
        if len(files) > SETTINGS.PATHS.MAX_TMP_FILES:
            logger.info(f"In folder {SETTINGS.PATHS.TMP_DIR} {len(files)} files, deleting all...")
            for file in files:
                try:
                    file.unlink()
                except Exception as e:
                    logger.error(e)
        else:
            logger.info(f"In folder {SETTINGS.PATHS.TMP_DIR} - {len(files)} files, do not delete...")
