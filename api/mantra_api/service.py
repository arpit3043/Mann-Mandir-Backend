from __future__ import annotations

import datetime as dt
from typing import List, Optional
from zoneinfo import ZoneInfo

from api.mantra_api.service_contract import MantraService
from clients.upstream import HavyakaApiClient, ShlokaApiClient
from core.pagination import paginate
from core.suggestions import ensure_found
from schemas.dtos import MantraDto
from services.static_registry import WEEKDAY_DEITIES, StaticContentRegistry

_IST = ZoneInfo("Asia/Kolkata")


def _fill_text(dto: MantraDto) -> MantraDto:
    if not dto.text:
        dto.text = dto.devanagari or dto.transliteration
    if not dto.devanagari and dto.text:
        dto.devanagari = dto.text
    return dto


def _map_havyaka(raw: dict) -> MantraDto:
    text = (
        str(raw.get("shloka") or raw.get("text") or raw.get("devanagari") or "") or None
    )
    return _fill_text(
        MantraDto(
            id=str(raw.get("_id") or raw.get("id") or "") or None,
            name=str(raw.get("name") or "") or None,
            text=text,
            devanagari=text,
            meaning=str(raw.get("purpose") or raw.get("meaning") or "") or None,
            deity=str(raw.get("godName") or raw.get("deity") or "") or None,
            veda=str(raw.get("veda") or "") or None,
            tags=raw.get("tags") if isinstance(raw.get("tags"), list) else None,
        )
    )


def _hindu_today(date: Optional[str] = None) -> dt.date:
    if date and date.strip():
        try:
            return dt.date.fromisoformat(date.strip())
        except ValueError as exc:
            raise ValueError(
                "Invalid date. Use YYYY-MM-DD, for example 2026-10-26"
            ) from exc
    return dt.datetime.now(_IST).date()


class DefaultMantraService(MantraService):
    def __init__(
        self,
        havyaka: HavyakaApiClient,
        shloka: ShlokaApiClient,
        static: StaticContentRegistry,
    ) -> None:
        self.havyaka = havyaka
        self.shloka = shloka
        self.static = static

    async def get_mantras(
        self, deity: Optional[str], page: int, size: int
    ) -> List[MantraDto]:
        fetch_limit = 200 if size > 200 else max(size * 5, 50)
        raw = await self.havyaka.get_mantras(limit=fetch_limit)
        mapped = [_map_havyaka(x) for x in (raw or [])]
        seen = {(m.name or "").strip().lower() for m in mapped if m.name}
        for row in self.static.get_mantras(None, limit=9999):
            dto = _fill_text(MantraDto.model_validate(row))
            key = (dto.name or "").strip().lower()
            if key and key in seen:
                continue
            mapped.append(dto)
            if key:
                seen.add(key)
        if deity and deity.strip():
            needle = deity.strip().lower()
            filtered = [m for m in mapped if (m.deity or "").lower() == needle]
            if not filtered:
                names = [item.deity for item in mapped if item.deity] + [
                    item.name for item in mapped if item.name
                ]
                ensure_found(
                    filtered, resource="Mantra", identifier=deity, available=names
                )
            mapped = filtered
        return paginate(mapped, page, size)

    async def get_random_mantra(self, date: Optional[str] = None) -> MantraDto:
        day = _hindu_today(date)
        weekday = day.weekday()
        english, hindi, ruling = WEEKDAY_DEITIES[weekday]
        row = self.static.get_weekday_mantra(weekday)
        dto = _fill_text(MantraDto.model_validate(row))
        dto.date = day.isoformat()
        dto.weekday = english
        dto.weekdayHindi = hindi
        dto.rulingDeity = ruling
        dto.deity = dto.deity or ruling
        tags = list(dto.tags or [])
        for extra in (english.lower(), hindi, ruling.lower(), "daily", "vara"):
            if extra not in tags:
                tags.append(extra)
        dto.tags = tags
        return dto
