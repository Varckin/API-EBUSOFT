from __future__ import annotations

from pathlib import Path
import uuid

from gtts import gTTS
from pydub import AudioSegment

from logger.init_logger import get_logger
from speech.settings import (
    TMP_DIR,
    MAX_TMP_FILES,
    TTS_DEFAULT_LANG,
    TTS_OUTPUT_FORMAT,
    TTS_OGG_CODEC,
)

logger = get_logger()


class TTS:
    def convert_text_to_voice(self, text: str, lang: str = TTS_DEFAULT_LANG) -> Path:
        """
        Generates audio from text. Returns path to the output file.
        Format and codecs are taken from settings.
        """
        self._check_tmp_files()

        name_file = uuid.uuid4().hex

        mp3_path = TMP_DIR / f"TTS_{name_file}.mp3"
        out_path = TMP_DIR / f"TTS_{name_file}.{TTS_OUTPUT_FORMAT}"

        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(str(mp3_path))

            audio = AudioSegment.from_mp3(mp3_path)

            if TTS_OUTPUT_FORMAT == "ogg":
                audio.export(out_path, format="ogg", codec=TTS_OGG_CODEC)
            else:
                audio.export(out_path, format=TTS_OUTPUT_FORMAT)

            return out_path
        except Exception as e:
            logger.error(e)
            return out_path if out_path.exists() else mp3_path

    def _check_tmp_files(self) -> None:
        files = [f for f in TMP_DIR.iterdir() if f.is_file()]
        if len(files) > MAX_TMP_FILES:
            logger.info(f"In folder {TMP_DIR} {len(files)} files, deleting all...")
            for file in files:
                try:
                    file.unlink()
                except Exception as e:
                    logger.error(e)
        else:
            logger.info(f"In folder {TMP_DIR} - {len(files)} files, do not delete...")
