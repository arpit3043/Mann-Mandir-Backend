from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class AartiDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    deity: str
    devanagari: Optional[str] = None
    transliteration: Optional[str] = None
    translation: Optional[str] = None
    language: Optional[str] = None
    audioUrl: Optional[str] = None
    verses: Optional[List[str]] = None


class ChalisaVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    verseNumber: int
    type: Optional[str] = None
    devanagari: Optional[str] = None
    transliteration: Optional[str] = None
    englishTranslation: Optional[str] = None
    hindiTranslation: Optional[str] = None
    tags: Optional[List[str]] = None


class ChalisaDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    deity: str
    title: str
    totalVerses: int
    verses: Optional[List[ChalisaVerseDto]] = None


class StotramVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    verseNumber: int
    sanskrit: Optional[str] = None
    transliteration: Optional[str] = None
    meaning: Optional[str] = None


class StotramDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    deity: str
    author: Optional[str] = None
    description: Optional[str] = None
    verseCount: int
    verses: Optional[List[StotramVerseDto]] = None


class MantraDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    name: Optional[str] = None
    text: Optional[str] = None
    devanagari: Optional[str] = None
    transliteration: Optional[str] = None
    meaning: Optional[str] = None
    deity: Optional[str] = None
    veda: Optional[str] = None
    tags: Optional[List[str]] = None


class GitaChapterDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    number: int
    name: str
    translation: Optional[str] = None
    transliteration: Optional[str] = None
    versesCount: int = 0
    summary: Optional[str] = None


class GitaVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bgId: Optional[str] = None
    chapter: int = 0
    verse: int = 0
    shloka: Optional[str] = None
    transliteration: Optional[str] = None
    translations: Optional[Dict[str, str]] = None
    commentaries: Optional[Dict[str, str]] = None


class RamayanaKandaDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    kandaId: str
    name: str
    description: Optional[str] = None
    sargas: int


class RamayanaVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    kandaId: str
    sarga: int
    verse: int
    original: Optional[str] = None
    transliteration: Optional[str] = None
    translation: Optional[str] = None


class MahabharataParvaDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    parvaNumber: int
    name: str
    description: Optional[str] = None
    chapters: int = 0
    verses: int = 0


class MahabharataVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    parva: int
    chapter: int
    verse: int
    text: Optional[str] = None
    translation: Optional[str] = None


class RigVedaVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    mandala: int = 0
    sukta: int = 0
    stanza: int = 0
    text: Optional[str] = None
    poet: Optional[str] = None
    deity: Optional[str] = None
    meter: Optional[str] = None
    poetCategory: Optional[str] = None
    deityCategory: Optional[str] = None


class VedaDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    vedaId: str
    name: str
    description: Optional[str] = None
    mandalas: int = 0
    hymns: int = 0
    verses: int = 0


class UpanishadDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    associatedVeda: Optional[str] = None
    description: Optional[str] = None
    chapters: int = 0


class UpanishadVerseDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    upanishadId: Optional[str] = None
    chapter: int = 0
    verse: int = 0
    sanskrit: Optional[str] = None
    transliteration: Optional[str] = None
    translation: Optional[str] = None
    commentary: Optional[str] = None


class SearchResultDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    type: str
    source: str
    title: str
    snippet: str = ""
    relevanceScore: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
