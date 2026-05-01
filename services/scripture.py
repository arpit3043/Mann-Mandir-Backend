from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from clients.upstream import DharmicDataClient, GitaTheAumClient, GitaVedicClient
from core.exceptions import ResourceNotFoundError
from core.pagination import JAVA_MAX_INT, paginate
from schemas.dtos import (
    GitaChapterDto,
    GitaVerseDto,
    MahabharataParvaDto,
    MahabharataVerseDto,
    RamayanaKandaDto,
    RamayanaVerseDto,
)
from services.static_registry import StaticContentRegistry

logger = logging.getLogger(__name__)


def _safe_get(m: Dict[str, Any], key: str) -> str:
    v = m.get(key)
    return "" if v is None else str(v)


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
            summary = None
    elif summary_raw is None:
        summary = None
    else:
        summary = str(summary_raw)
    num = c.get("chapter_number")
    if num is None:
        num = c.get("number")
    vc = c.get("verses_count")
    if vc is None:
        vc = c.get("versesCount") or 0
    return GitaChapterDto(
        number=int(num),
        name=str(c.get("name", "")),
        translation=c.get("translation"),
        transliteration=c.get("transliteration"),
        versesCount=int(vc),
        summary=summary,
    )


def _map_vedic_chapter_row(c: Dict[str, Any]) -> GitaChapterDto:
    return GitaChapterDto(
        number=int(c.get("chapter_number", 0)),
        name=str(c.get("name", "")),
        translation=c.get("translation"),
        transliteration=None,
        versesCount=int(c.get("verses_count", 0)),
        summary=None,
    )


def _enrich_theaum_verse(v: Dict[str, Any], chapter: int) -> GitaVerseDto:
    return GitaVerseDto(
        bgId=v.get("bg_id") or v.get("bgId"),
        chapter=chapter,
        verse=int(v.get("verse", 0)),
        shloka=v.get("shloka"),
    )


class DefaultScriptureService:
    def __init__(
        self,
        gita_theaum: GitaTheAumClient,
        gita_vedic: GitaVedicClient,
        dharmic: DharmicDataClient,
        static: StaticContentRegistry,
    ) -> None:
        self._theaum = gita_theaum
        self._vedic = gita_vedic
        self._dharmic = dharmic
        self._static = static

    async def get_gita_chapters(self) -> List[GitaChapterDto]:
        resp = await self._theaum.get_all_chapters()
        if resp:
            return [_map_theaum_chapter(c) for c in resp]
        logger.warning("TheAum chapters API unavailable, trying VedicScriptures fallback")
        vedic = await self._vedic.get_all_chapters()
        if vedic:
            return [_map_vedic_chapter_row(c) for c in vedic]
        return [GitaChapterDto.model_validate(x) for x in self._static.get_gita_chapters()]

    async def get_gita_chapter(self, chapter_number: int) -> GitaChapterDto:
        one = await self._theaum.get_chapter(chapter_number)
        if one:
            return _map_theaum_chapter(one)
        chapters = await self.get_gita_chapters()
        for c in chapters:
            if c.number == chapter_number:
                return c
        raise ResourceNotFoundError("Gita chapter", str(chapter_number))

    async def get_gita_verses_by_chapter(self, chapter_number: int) -> List[GitaVerseDto]:
        resp = await self._theaum.get_chapter_verses(chapter_number)
        if not resp:
            raise ResourceNotFoundError("Gita chapter verses", str(chapter_number))
        return [_enrich_theaum_verse(v, chapter_number) for v in resp]

    async def get_gita_verse(self, chapter_number: int, verse_number: int) -> GitaVerseDto:
        vedic_resp = await self._vedic.get_slok(chapter_number, verse_number)
        translations_raw = await self._theaum.get_verse_translations(chapter_number, verse_number)
        commentary_raw = await self._theaum.get_verse_commentary(chapter_number, verse_number)

        translations: Dict[str, str] = {}
        if translations_raw and isinstance(translations_raw.get("translations"), dict):
            translations = dict(translations_raw["translations"])
        commentaries: Dict[str, str] = {}
        if commentary_raw and isinstance(commentary_raw.get("commentaries"), dict):
            commentaries = dict(commentary_raw["commentaries"])

        if vedic_resp:
            tej = vedic_resp.get("tej")
            if isinstance(tej, dict):
                translations["tej"] = _safe_get(tej, "ht")
            siva = vedic_resp.get("siva")
            if isinstance(siva, dict):
                translations["siva"] = _safe_get(siva, "et")
            chinmay = vedic_resp.get("chinmay")
            if isinstance(chinmay, dict):
                translations["chinmay"] = _safe_get(chinmay, "hc")

        shloka = ""
        if vedic_resp:
            shloka = str(vedic_resp.get("slok", "") or "")

        return GitaVerseDto(
            bgId=f"{chapter_number}.{verse_number}",
            chapter=chapter_number,
            verse=verse_number,
            shloka=shloka,
            translations=translations or None,
            commentaries=commentaries or None,
        )

    async def get_ramayana_kandas(self) -> List[RamayanaKandaDto]:
        return [RamayanaKandaDto.model_validate(x) for x in self._static.get_ramayana_kandas()]

    async def get_ramayana_kanda(self, kanda_id: str) -> RamayanaKandaDto:
        for k in self._static.get_ramayana_kandas():
            if str(k.get("kandaId", "")).lower() == kanda_id.lower():
                return RamayanaKandaDto.model_validate(k)
        raise ResourceNotFoundError("Ramayana kanda", kanda_id)

    def _parse_ramayana_verses(self, data: Dict[str, Any], kanda_id: str, sarga: int) -> List[RamayanaVerseDto]:
        out: List[RamayanaVerseDto] = []
        try:
            sargas = data.get("sargas")
            if not isinstance(sargas, list) or sarga - 1 >= len(sargas):
                return out
            sarga_data = sargas[sarga - 1]
            if not isinstance(sarga_data, dict):
                return out
            verses = sarga_data.get("verses")
            if not isinstance(verses, list):
                return out
            for i, v in enumerate(verses):
                if not isinstance(v, dict):
                    continue
                out.append(
                    RamayanaVerseDto(
                        kandaId=kanda_id,
                        sarga=sarga,
                        verse=i + 1,
                        original=str(v.get("text", "")),
                        translation=str(v.get("translation", "")),
                    )
                )
        except Exception as e:
            logger.error("Error parsing Ramayana data: %s", e)
        return out

    def _parse_mahabharata_verses(
        self, data: Dict[str, Any], parva: int, chapter: int
    ) -> List[MahabharataVerseDto]:
        out: List[MahabharataVerseDto] = []
        try:
            chapters = data.get("chapters")
            if not isinstance(chapters, list) or chapter - 1 >= len(chapters):
                return out
            ch_data = chapters[chapter - 1]
            if not isinstance(ch_data, dict):
                return out
            verses = ch_data.get("verses")
            if not isinstance(verses, list):
                return out
            for i, v in enumerate(verses):
                if not isinstance(v, dict):
                    continue
                out.append(
                    MahabharataVerseDto(
                        parva=parva,
                        chapter=chapter,
                        verse=i + 1,
                        text=str(v.get("text", "")),
                        translation=str(v.get("translation", "")),
                    )
                )
        except Exception as e:
            logger.error("Error parsing Mahabharata data: %s", e)
        return out

    async def get_ramayana_verses(
        self, kanda_id: str, sarga: int, page: int, size: int
    ) -> List[RamayanaVerseDto]:
        raw = await self._dharmic.get_ramayana_kanda(kanda_id)
        if raw:
            all_v = self._parse_ramayana_verses(raw, kanda_id, sarga)
        else:
            all_v = [
                RamayanaVerseDto.model_validate(x)
                for x in self._static.get_ramayana_verses(kanda_id, sarga)
            ]
        return paginate(all_v, page, size)

    async def get_ramayana_verse(self, kanda_id: str, sarga: int, verse: int) -> RamayanaVerseDto:
        all_v = await self.get_ramayana_verses(kanda_id, sarga, 0, JAVA_MAX_INT)
        for v in all_v:
            if v.verse == verse:
                return v
        raise ResourceNotFoundError("Ramayana verse", f"{kanda_id}/{sarga}/{verse}")

    async def get_mahabharata_parvas(self) -> List[MahabharataParvaDto]:
        return [MahabharataParvaDto.model_validate(x) for x in self._static.get_mahabharata_parvas()]

    async def get_mahabharata_parva(self, parva_number: int) -> MahabharataParvaDto:
        for p in self._static.get_mahabharata_parvas():
            if int(p.get("parvaNumber", -1)) == parva_number:
                return MahabharataParvaDto.model_validate(p)
        raise ResourceNotFoundError("Mahabharata parva", str(parva_number))

    async def get_mahabharata_verses(
        self, parva_number: int, chapter_number: int, page: int, size: int
    ) -> List[MahabharataVerseDto]:
        raw = await self._dharmic.get_mahabharata_parva(parva_number)
        if raw:
            all_v = self._parse_mahabharata_verses(raw, parva_number, chapter_number)
        else:
            all_v = [
                MahabharataVerseDto.model_validate(x)
                for x in self._static.get_mahabharata_verses(parva_number, chapter_number)
            ]
        return paginate(all_v, page, size)

    async def get_mahabharata_verse(
        self, parva_number: int, chapter_number: int, verse: int
    ) -> MahabharataVerseDto:
        all_v = await self.get_mahabharata_verses(parva_number, chapter_number, 0, JAVA_MAX_INT)
        for v in all_v:
            if v.verse == verse:
                return v
        raise ResourceNotFoundError("Mahabharata verse", f"{parva_number}/{chapter_number}/{verse}")
