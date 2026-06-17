from typing import Any, Dict, List, Optional

from api.scriptures_api.gita_api.service_contract import GitaService
from clients.upstream import GitaTheAumClient, GitaVedicClient
from core.exceptions import ResourceNotFoundError
from schemas.dtos import GitaChapterDto, GitaVerseDto
from services.static_registry import StaticContentRegistry


def _map_theaum_chapter(c: Dict[str, Any]) -> GitaChapterDto:
    summary_raw = c.get("summary")
    summary: Optional[str]
    if isinstance(summary_raw, dict):
        english = summary_raw.get("en")
        if english is not None:
            summary = str(english)
        elif summary_raw:
            summary = str(next(iter(summary_raw.values())))
        else:
            summary = ""
    else:
        summary = str(summary_raw) if summary_raw else ""

    return GitaChapterDto(
        number=int(c.get("chapter_number", 0)),
        name=str(c.get("name", "")),
        translation=str(c.get("translation", "")),
        transliteration=str(c.get("transliteration", "")),
        meaning=str(c.get("meaning", {}).get("en", "")),
        summary=summary,
        versesCount=int(c.get("verses_count", 0)),
    )


class DefaultGitaService(GitaService):
    def __init__(
        self,
        gita_theaum: GitaTheAumClient,
        gita_vedic: GitaVedicClient,
        static: StaticContentRegistry,
    ) -> None:
        self._gita_theaum = gita_theaum
        self._gita_vedic = gita_vedic
        self._static = static

    async def get_gita_chapters(self) -> List[GitaChapterDto]:
        raw = await self._gita_theaum.get_all_chapters()
        if raw:
            return [_map_theaum_chapter(x) for x in raw]
        raw = self._static.get_gita_chapters()
        return [_map_theaum_chapter(x) for x in raw]

    async def get_gita_chapter(self, chapter_number: int) -> GitaChapterDto:
        raw = await self._gita_theaum.get_chapter(chapter_number)
        if raw:
            return _map_theaum_chapter(raw)
        chaps = self._static.get_gita_chapters()
        for x in chaps:
            if x.get("chapter_number") == chapter_number:
                return _map_theaum_chapter(x)
        raise ResourceNotFoundError("Gita chapter", str(chapter_number))

    async def get_gita_verses_by_chapter(self, chapter_number: int) -> List[GitaVerseDto]:
        raw = await self._gita_vedic.get_verses_for_chapter(chapter_number)
        if raw:
            out = []
            for v in raw:
                out.append(
                    GitaVerseDto(
                        chapter=chapter_number,
                        verse=int(v.get("verse", 0)),
                        text=str(v.get("text", "")),
                        transliteration=str(v.get("transliteration", "")),
                        wordMeanings=str(v.get("word_meanings", "")),
                    )
                )
            return out
        static_verses = self._static.get_gita_verses(chapter_number)
        return [GitaVerseDto.model_validate(x) for x in static_verses]

    async def get_gita_verse(self, chapter_number: int, verse_number: int) -> GitaVerseDto:
        v = await self._gita_vedic.get_slok(chapter_number, verse_number)
        if v:
            return GitaVerseDto(
                chapter=chapter_number,
                verse=verse_number,
                text=str(v.get("text", "")),
                transliteration=str(v.get("transliteration", "")),
                wordMeanings=str(v.get("word_meanings", "")),
            )
        verses = self._static.get_gita_verses(chapter_number)
        for vr in verses:
            if vr.get("verse") == verse_number:
                return GitaVerseDto.model_validate(vr)
        raise ResourceNotFoundError("Gita verse", f"{chapter_number}.{verse_number}")
