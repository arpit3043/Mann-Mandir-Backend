from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from clients.upstream import HanumanChalisaClient, HavyakaApiClient, ShlokaApiClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import AartiDto, ChalisaDto, ChalisaVerseDto, MantraDto, StotramDto
from services.static_registry import StaticContentRegistry

logger = logging.getLogger(__name__)


def _chalisa_verse_from_api(row: Dict[str, Any]) -> ChalisaVerseDto:
    eng = row.get("english_translation")
    if not eng and row.get("translations"):
        for t in row["translations"]:
            if not isinstance(t, dict):
                continue
            typ = str(t.get("translation_type", "")).lower()
            if "english" in typ:
                eng = t.get("translation")
                break
        if not eng and row["translations"]:
            first = row["translations"][0]
            if isinstance(first, dict):
                eng = first.get("translation")
    num = row.get("id")
    if num is None:
        num = row.get("number", 0)
    return ChalisaVerseDto(
        verseNumber=int(num),
        type=row.get("type"),
        devanagari=row.get("verse") or row.get("devanagari"),
        transliteration=row.get("transliteration"),
        englishTranslation=eng,
        hindiTranslation=row.get("hindi_translation"),
        tags=row.get("tags") or [],
    )


def _havyaka_to_mantra(raw: Dict[str, Any]) -> MantraDto:
    return MantraDto(
        id=str(raw.get("_id", "")),
        name=str(raw.get("name", "")),
        text=str(raw.get("shloka", "")),
        meaning=str(raw.get("purpose", "")),
        deity=str(raw.get("godName", "")),
        tags=[],
    )


class DefaultGodService:
    def __init__(
        self,
        hanuman: HanumanChalisaClient,
        havyaka: HavyakaApiClient,
        shloka: ShlokaApiClient,
        static: StaticContentRegistry,
    ) -> None:
        self._hanuman = hanuman
        self._havyaka = havyaka
        self._shloka = shloka
        self._static = static

    async def get_aartis(self, deity: Optional[str], page: int, size: int) -> List[AartiDto]:
        all_rows = self._static.get_all_aartis()
        if deity and deity.strip():
            d = deity.strip().lower()
            all_rows = [a for a in all_rows if str(a.get("deity", "")).lower() == d]
        page_rows = paginate(all_rows, page, size)
        return [AartiDto.model_validate(x) for x in page_rows]

    async def get_aarti_by_id(self, aarti_id: str) -> AartiDto:
        for a in self._static.get_all_aartis():
            if a.get("id") == aarti_id:
                return AartiDto.model_validate(a)
        raise ResourceNotFoundError("Aarti", aarti_id)

    async def get_aarti_deities(self) -> List[str]:
        return sorted({str(a["deity"]) for a in self._static.get_all_aartis() if a.get("deity")})

    async def get_chalisas(self, page: int, size: int) -> List[ChalisaDto]:
        rows = paginate(self._static.get_all_chalisas(), page, size)
        return [ChalisaDto.model_validate(x) for x in rows]

    async def _fetch_hanuman_chalisa(self) -> ChalisaDto:
        verses_raw = await self._hanuman.get_all_verses()
        if not verses_raw:
            logger.warning("Hanuman Chalisa API unavailable, using static fallback")
            verses_raw = self._static.get_hanuman_chalisa_verses()
        verses = [_chalisa_verse_from_api(v) for v in verses_raw]
        return ChalisaDto(
            id="hanuman-chalisa",
            deity="Hanuman",
            title="Hanuman Chalisa",
            totalVerses=len(verses),
            verses=verses,
        )

    async def get_chalisa_by_deity(self, deity: str) -> ChalisaDto:
        if deity.lower() == "hanuman":
            return await self._fetch_hanuman_chalisa()
        row = self._static.get_chalisa_by_deity(deity)
        if row:
            return ChalisaDto.model_validate(row)
        raise ResourceNotFoundError("Chalisa", deity)

    async def get_chalisa_verse(self, deity: str, verse_number: int) -> ChalisaVerseDto:
        if deity.lower() == "hanuman":
            verses = await self._hanuman.get_all_verses()
            if not verses:
                verses = self._static.get_hanuman_chalisa_verses()
            for v in verses:
                num = v.get("id", v.get("number"))
                if num is not None and int(num) == verse_number:
                    return _chalisa_verse_from_api(v)
            raise ResourceNotFoundError("Chalisa verse", str(verse_number))
        chalisa = await self.get_chalisa_by_deity(deity)
        if not chalisa.verses:
            raise ResourceNotFoundError("Chalisa verse", str(verse_number))
        for vr in chalisa.verses:
            if vr.verseNumber == verse_number:
                return vr
        raise ResourceNotFoundError("Chalisa verse", str(verse_number))

    async def get_stotrams(self, deity: Optional[str], page: int, size: int) -> List[StotramDto]:
        rows = self._static.get_all_stotrams()
        if deity and deity.strip():
            d = deity.strip().lower()
            rows = [s for s in rows if str(s.get("deity", "")).lower() == d]
        page_rows = paginate(rows, page, size)
        return [StotramDto.model_validate(x) for x in page_rows]

    async def get_stotram_by_id(self, stotram_id: str) -> StotramDto:
        for s in self._static.get_all_stotrams():
            if s.get("id") == stotram_id:
                return StotramDto.model_validate(s)
        raise ResourceNotFoundError("Stotram", stotram_id)

    async def get_random_mantra(self) -> MantraDto:
        r = await self._shloka.get_random_shloka()
        if r:
            return MantraDto(
                id=r.get("id"),
                text=r.get("text"),
                meaning=r.get("meaning"),
                deity=r.get("deity"),
                veda=r.get("source"),
            )
        return MantraDto.model_validate(self._static.get_random_mantra())

    async def get_mantras(self, deity: Optional[str], limit: int) -> List[MantraDto]:
        raw: Optional[List[Dict[str, Any]]]
        if deity:
            raw = await self._havyaka.get_mantras_by_name(deity, limit)
        else:
            raw = await self._havyaka.get_mantras(limit)
        if raw:
            return [_havyaka_to_mantra(x) for x in raw][:limit]
        rows = self._static.get_mantras(deity, limit)
        return [MantraDto.model_validate(x) for x in rows]
