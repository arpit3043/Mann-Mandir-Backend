from typing import Any, Dict, List, Optional

import asyncio

from api.scriptures_api.gita_api.service_contract import GitaService
from clients.upstream import GitaTheAumClient, GitaVedicClient
from core.exceptions import ResourceNotFoundError
from schemas.dtos import GitaChapterDto, GitaVerseDto
from services.static_registry import StaticContentRegistry


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
        number=_as_int(c.get("chapter_number", c.get("number"))),
        name=str(c.get("name", "")),
        translation=str(c.get("translation", "")),
        transliteration=str(c.get("transliteration", "")),
        summary=summary,
        versesCount=_as_int(c.get("verses_count", c.get("versesCount"))),
    )


def _map_gita_verse(chapter_number: int, v: Dict[str, Any], verse_number: Optional[int] = None) -> GitaVerseDto:
    verse = verse_number if verse_number is not None else _as_int(v.get("verse"))
    translations: Dict[str, str] = {}
    if isinstance(v.get("translations"), dict):
        translations = {str(k): str(val) for k, val in v["translations"].items() if val}
    siva = v.get("siva") if isinstance(v.get("siva"), dict) else {}
    tej = v.get("tej") if isinstance(v.get("tej"), dict) else {}
    if siva.get("et"):
        translations.setdefault("en", str(siva["et"]))
    if tej.get("ht"):
        translations.setdefault("hi", str(tej["ht"]))
    if v.get("wordMeanings"):
        translations.setdefault("en", str(v.get("wordMeanings")))
    if v.get("word_meanings"):
        translations.setdefault("en", str(v.get("word_meanings")))

    commentaries: Dict[str, str] = {}
    if isinstance(v.get("commentaries"), dict):
        commentaries = {str(k): str(val) for k, val in v["commentaries"].items() if val}

    return GitaVerseDto(
        bgId=str(v.get("bgId") or v.get("_id") or f"BG{chapter_number}.{verse}"),
        chapter=_as_int(v.get("chapter"), chapter_number),
        verse=verse,
        shloka=str(v.get("slok") or v.get("shloka") or v.get("text") or "") or None,
        transliteration=str(v.get("transliteration") or "") or None,
        translations=translations or None,
        commentaries=commentaries or None,
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

    def _static_chapters(self) -> List[GitaChapterDto]:
        return [_map_theaum_chapter(x) for x in self._static.get_gita_chapters()]

    async def get_gita_chapters(self) -> List[GitaChapterDto]:
        raw = await self._gita_theaum.get_all_chapters()
        if raw:
            return [_map_theaum_chapter(x) for x in raw]
        return self._static_chapters()

    async def get_gita_chapter(self, chapter_number: int) -> GitaChapterDto:
        raw = await self._gita_theaum.get_chapter(chapter_number)
        if raw:
            return _map_theaum_chapter(raw)
        for mapped in self._static_chapters():
            if mapped.number == chapter_number:
                return mapped
        raise ResourceNotFoundError("Gita chapter", str(chapter_number))

    async def get_gita_verses_by_chapter(self, chapter_number: int) -> List[GitaVerseDto]:
        raw = await self._gita_vedic.get_verses_for_chapter(chapter_number)
        if isinstance(raw, list) and raw:
            return [_map_gita_verse(chapter_number, v) for v in raw if isinstance(v, dict)]

        try:
            chapter = await self.get_gita_chapter(chapter_number)
            count = chapter.versesCount
        except ResourceNotFoundError:
            count = 0

        if count > 0:
            sem = asyncio.Semaphore(8)

            async def fetch_one(n: int) -> Optional[Dict[str, Any]]:
                async with sem:
                    return await self._gita_vedic.get_slok(chapter_number, n)

            fetched = await asyncio.gather(*[fetch_one(i) for i in range(1, count + 1)])
            out = [
                _map_gita_verse(chapter_number, v, verse_number=i)
                for i, v in enumerate(fetched, start=1)
                if isinstance(v, dict)
            ]
            if out:
                return out

        static_verses = self._static.get_gita_verses(chapter_number)
        return [GitaVerseDto.model_validate(x) for x in static_verses]

    async def get_gita_verse(self, chapter_number: int, verse_number: int) -> GitaVerseDto:
        v = await self._gita_vedic.get_slok(chapter_number, verse_number)
        if v:
            return _map_gita_verse(chapter_number, v, verse_number=verse_number)
        verses = self._static.get_gita_verses(chapter_number)
        for vr in verses:
            if _as_int(vr.get("verse")) == verse_number:
                return GitaVerseDto.model_validate(vr)
        raise ResourceNotFoundError("Gita verse", f"{chapter_number}.{verse_number}")
