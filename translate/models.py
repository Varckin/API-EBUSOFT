from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any


class PronunciationModel(BaseModel):
    source_text_phonetic: Optional[str]
    source_text_audio: Optional[HttpUrl]
    destination_text_audio: Optional[HttpUrl]


class TranslationPair(BaseModel):
    key: str
    values: List[str]


class TranslationsModel(BaseModel):
    all_translations: Optional[List[List[Any]]]  # since it's nested lists
    possible_translations: Optional[List[str]]
    possible_mistakes: Optional[List[str]]


class DefinitionSynonyms(BaseModel):
    __root__: Dict[str, List[str]]


class DefinitionModel(BaseModel):
    part_of_speech: str
    definition: str
    example: Optional[str]
    other_examples: Optional[List[str]]
    synonyms: Optional[DefinitionSynonyms]


class TranslateResponse(BaseModel):
    source_language: str
    source_text: str
    destination_language: str
    destination_text: str
    pronunciation: PronunciationModel
    translations: TranslationsModel
    definitions: Optional[List[DefinitionModel]]
    see_also: Optional[List[str]]


class TranslateRequest(BaseModel):
    sl: Optional[str] = None
    dl: str
    text: str
