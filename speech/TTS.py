from __future__ import annotations

from pathlib import Path
import uuid

from gtts import gTTS
from pydub import AudioSegment

from logger.init_logger import get_logger
from speech.settings import SETTINGS

logger = get_logger("TTS")


class TTS:
    def convert_text_to_voice(self, text: str, lang: str) -> Path:
        """
        Generates audio from text. Returns path to the output file.
        Format and codecs are taken from settings.
        """
        self._check_tmp_files()

        name_file = uuid.uuid4().hex

        mp3_path = SETTINGS.PATHS.TMP_DIR / f"TTS_{name_file}.mp3"
        out_path = SETTINGS.PATHS.TMP_DIR / f"TTS_{name_file}.{SETTINGS.TTS.OUTPUT_FORMAT}"

        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(str(mp3_path))

            audio = AudioSegment.from_mp3(mp3_path)

            if SETTINGS.TTS.OUTPUT_FORMAT == "ogg":
                audio.export(out_path, format="ogg", codec=SETTINGS.TTS.OGG_CODEC)
            else:
                audio.export(out_path, format=SETTINGS.TTS.OUTPUT_FORMAT)

            return out_path
        except Exception as e:
            logger.error(e)
            return out_path if out_path.exists() else mp3_path

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
