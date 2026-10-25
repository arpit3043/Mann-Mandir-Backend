from __future__ import annotations

import asyncio
import logging
import random
import re
from typing import Any, Dict, List

from clients.upstream import DharmicDataClient, HavyakaApiClient, RigVedaApiClient
from core.exceptions import ResourceNotFoundError
from core.pagination import JAVA_MAX_INT, paginate
from core.suggestions import ensure_found, suggestion_for
from schemas.dtos import MantraDto, RigVedaVerseDto, UpanishadDto, UpanishadVerseDto, VedaDto
from services.static_registry import StaticContentRegistry

logger = logging.getLogger(__name__)

_STANZA_SPLIT = re.compile(r"॥\s*[0-9०-९]+\s*॥")
_YAJUR_SPLIT = re.compile(r"।{2}\s*\d+\s*।{2}")


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _split_stanzas(text: str) -> List[str]:
    parts = [p.strip() for p in _STANZA_SPLIT.split(text or "") if p.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _map_rig_verse(r: Dict[str, Any]) -> RigVedaVerseDto:
    return RigVedaVerseDto(
        mandala=_as_int(r.get("mandala", r.get("mandal"))),
        sukta=_as_int(r.get("sukta")),
        stanza=_as_int(r.get("stanza"), 1),
        text=r.get("text") or r.get("sanskrit"),
        poet=r.get("sungby") or r.get("poet"),
        poetCategory=r.get("sungbycategory") or r.get("poetCategory"),
        deity=r.get("sungfor") or r.get("deity"),
        deityCategory=r.get("sungforcategory") or r.get("deityCategory"),
        meter=r.get("meter"),
    )


def _map_dharmic_sukta(r: Dict[str, Any]) -> List[RigVedaVerseDto]:
    mandala = _as_int(r.get("mandala"))
    sukta = _as_int(r.get("sukta"))
    chunks = _split_stanzas(str(r.get("text") or ""))
    if not chunks:
        return []
    return [
        RigVedaVerseDto(mandala=mandala, sukta=sukta, stanza=i, text=chunk)
        for i, chunk in enumerate(chunks, start=1)
    ]


def _map_havyaka_mantra(raw: Dict[str, Any]) -> MantraDto:
    text = str(raw.get("shloka") or raw.get("text") or raw.get("devanagari") or "")
    return MantraDto(
        id=str(raw.get("_id") or raw.get("id") or ""),
        name=str(raw.get("name", "")) or None,
        text=text or None,
        devanagari=text or None,
        meaning=str(raw.get("purpose") or raw.get("meaning") or "") or None,
        deity=str(raw.get("godName") or raw.get("deity") or "") or None,
        tags=[],
    )


def _mantras_from_rows(rows: List[Dict[str, Any]], veda_name: str) -> List[MantraDto]:
    result: List[MantraDto] = []
    for i, m in enumerate(rows):
        if not isinstance(m, dict):
            continue
        text = str(m.get("text") or "")
        if veda_name.lower() == "yajur":
            chunks = [c.strip() for c in _YAJUR_SPLIT.split(text) if c.strip()]
            adhyaya = _as_int(m.get("adhyaya"), i + 1)
            if not chunks:
                chunks = [text] if text else []
            for idx, chunk in enumerate(chunks, start=1):
                result.append(
                    MantraDto(
                        id=f"yajur_{adhyaya}_{idx}",
                        name=f"Yajur Veda Adhyaya {adhyaya}.{idx}",
                        text=chunk,
                        veda="Yajur",
                    )
                )
            continue
        result.append(
            MantraDto(
                id=str(m.get("id") or f"{veda_name.lower()}_{i + 1}"),
                name=str(m.get("name") or m.get("deity") or "") or None,
                text=text or None,
                meaning=str(m.get("meaning") or "") or None,
                deity=str(m.get("deity") or "") or None,
                veda=veda_name,
            )
        )
    return result


class DefaultVedaService:
    def __init__(
        self,
        rig: RigVedaApiClient,
        havyaka: HavyakaApiClient,
        dharmic: DharmicDataClient,
        static: StaticContentRegistry,
    ) -> None:
        self._rig = rig
        self._havyaka = havyaka
        self._dharmic = dharmic
        self._static = static

    async def get_all_vedas(self) -> List[VedaDto]:
        return [VedaDto.model_validate(x) for x in self._static.get_all_vedas()]

    async def get_veda(self, veda_id: str) -> VedaDto:
        for v in self._static.get_all_vedas():
            if str(v.get("vedaId", "")).lower() == veda_id.lower():
                return VedaDto.model_validate(v)
        names = [str(item.get("vedaId") or item.get("name") or "") for item in self._static.get_all_vedas()]
        raise ResourceNotFoundError("Veda", veda_id, suggestion=suggestion_for(veda_id, names))

    async def get_rig_veda_by_mandala(self, mandala: int, page: int, size: int) -> List[RigVedaVerseDto]:
        dharmic = await self._dharmic.get_rig_veda_mandala(mandala)
        if dharmic:
            all_v = [verse for row in dharmic for verse in _map_dharmic_sukta(row)]
        else:
            api_list = await self._rig.get_by_mandala(mandala)
            if api_list:
                all_v = [_map_rig_verse(x) for x in api_list]
            else:
                all_v = [RigVedaVerseDto.model_validate(x) for x in self._static.get_rig_veda_verses(mandala)]
        if not all_v:
            raise ResourceNotFoundError(
                "Rig Veda mandala",
                str(mandala),
                suggestion="Try searching: 1",
            )
        return paginate(all_v, page, size)

    async def get_rig_veda_by_deity(self, deity: str, page: int, size: int) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_deity(deity)
        if api_list:
            all_v = [_map_rig_verse(x) for x in api_list]
        else:
            needle = deity.strip().lower()
            all_v = [
                RigVedaVerseDto.model_validate(x)
                for x in self._static.get_rig_veda_verses(None)
                if str(x.get("deity", "")).lower() == needle
            ]
        if not all_v:
            names = [str(x.get("deity") or "") for x in self._static.get_rig_veda_verses(None)]
            ensure_found(all_v, resource="Rig Veda deity", identifier=deity, available=names)
        return paginate(all_v, page, size)

    async def get_rig_veda_by_poet(self, poet: str, page: int, size: int) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_poet(poet)
        if api_list:
            all_v = [_map_rig_verse(x) for x in api_list]
        else:
            needle = poet.strip().lower()
            all_v = [
                RigVedaVerseDto.model_validate(x)
                for x in self._static.get_rig_veda_verses(None)
                if str(x.get("poet", "")).lower() == needle
            ]
        if not all_v:
            names = [str(x.get("poet") or "") for x in self._static.get_rig_veda_verses(None)]
            ensure_found(all_v, resource="Rig Veda poet", identifier=poet, available=names)
        return paginate(all_v, page, size)

    async def get_rig_veda_verse(self, mandala: int, sukta: int, stanza: int) -> RigVedaVerseDto:
        all_v = await self.get_rig_veda_by_mandala(mandala, 0, JAVA_MAX_INT)
        for v in all_v:
            if v.sukta == sukta and v.stanza == stanza:
                return v
        raise ResourceNotFoundError("Rig Veda verse", f"{mandala}/{sukta}/{stanza}")

    async def get_yajur_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._dharmic.get_yajur_veda()
        if raw:
            all_m = _mantras_from_rows(raw, "Yajur")
        else:
            all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("yajur")]
        return paginate(all_m, page, size)

    async def get_sama_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._dharmic.get_sama_veda()
        if raw:
            all_m = _mantras_from_rows(raw, "Sama")
        else:
            havyaka = await self._havyaka.get_mantras_by_name("sama", 500)
            if havyaka:
                all_m = [_map_havyaka_mantra(x) for x in havyaka]
            else:
                all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("sama")]
        return paginate(all_m, page, size)

    async def get_atharva_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        sem = asyncio.Semaphore(4)

        async def load_kanda(kanda: int) -> List[Dict[str, Any]]:
            async with sem:
                rows = await self._dharmic.get_atharva_veda(kanda)
                return rows or []

        loaded = await asyncio.gather(*[load_kanda(k) for k in range(1, 6)])
        rows = [item for group in loaded for item in group]
        if rows:
            all_m = _mantras_from_rows(rows, "Atharva")
        else:
            all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("atharva")]
        return paginate(all_m, page, size)

    async def get_upanishads(self) -> List[UpanishadDto]:
        return [UpanishadDto.model_validate(x) for x in self._static.get_all_upanishads()]

    async def get_upanishad(self, upanishad_id: str) -> UpanishadDto:
        for u in self._static.get_all_upanishads():
            if str(u.get("id", "")).lower() == upanishad_id.lower():
                return UpanishadDto.model_validate(u)
        names = [str(item.get("id") or item.get("name") or "") for item in self._static.get_all_upanishads()]
        raise ResourceNotFoundError("Upanishad", upanishad_id, suggestion=suggestion_for(upanishad_id, names))

    async def get_upanishad_verses(
        self, upanishad_id: str, chapter: int, page: int, size: int
    ) -> List[UpanishadVerseDto]:
        await self.get_upanishad(upanishad_id)
        rows = self._static.get_upanishad_verses(upanishad_id, chapter)
        if not rows:
            raise ResourceNotFoundError(
                "Upanishad chapter",
                f"{upanishad_id}/{chapter}",
                suggestion="Try searching: 1",
            )
        return paginate([UpanishadVerseDto.model_validate(x) for x in rows], page, size)

    async def get_upanishad_verse(self, upanishad_id: str, chapter: int, verse: int) -> UpanishadVerseDto:
        all_v = await self.get_upanishad_verses(upanishad_id, chapter, 0, JAVA_MAX_INT)
        for v in all_v:
            if v.verse == verse:
                return v
        raise ResourceNotFoundError("Upanishad verse", f"{upanishad_id}/{chapter}/{verse}")

    async def get_random_vedic_mantra(self) -> MantraDto:
        pool = self._static.get_veda_mantras(None)
        if not pool:
            return MantraDto(text="ॐ", meaning="The primordial sound")
        return MantraDto.model_validate(random.choice(pool))

    async def search_mantras(self, deity: str, limit: int) -> List[MantraDto]:
        raw = await self._havyaka.get_mantras_by_name(deity, limit)
        if raw:
            return [_map_havyaka_mantra(x) for x in raw][:limit]
        rows = self._static.get_mantras(deity, limit)
        mapped = [MantraDto.model_validate(x) for x in rows]
        if mapped:
            return mapped
        pool = self._static.get_mantras(None, 9999)
        names = [str(item.get("deity") or "") for item in pool] + [str(item.get("name") or "") for item in pool]
        ensure_found(mapped, resource="Mantra", identifier=deity, available=names)
