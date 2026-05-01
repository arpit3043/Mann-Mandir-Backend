from __future__ import annotations

import logging
import random
from typing import Any, Dict, List

from clients.upstream import DharmicDataClient, HavyakaApiClient, RigVedaApiClient
from core.exceptions import ResourceNotFoundError
from core.pagination import JAVA_MAX_INT, paginate
from schemas.dtos import MantraDto, RigVedaVerseDto, UpanishadDto, UpanishadVerseDto, VedaDto
from services.static_registry import StaticContentRegistry

logger = logging.getLogger(__name__)


def _map_rig_verse(r: Dict[str, Any]) -> RigVedaVerseDto:
    return RigVedaVerseDto(
        mandala=int(r.get("mandal", 0)),
        sukta=int(r.get("sukta", 0)),
        stanza=int(r.get("stanza", 0)),
        poet=r.get("sungby"),
        poetCategory=r.get("sungbycategory"),
        deity=r.get("sungfor"),
        deityCategory=r.get("sungforcategory"),
        meter=r.get("meter"),
    )


def _map_havyaka_mantra(raw: Dict[str, Any]) -> MantraDto:
    return MantraDto(
        id=str(raw.get("_id", "")),
        name=str(raw.get("name", "")),
        text=str(raw.get("shloka", "")),
        meaning=str(raw.get("purpose", "")),
        deity=str(raw.get("godName", "")),
        tags=[],
    )


def _parse_veda_mantras(data: Dict[str, Any], veda_name: str) -> List[MantraDto]:
    result: List[MantraDto] = []
    try:
        mantras = data.get("mantras")
        if not isinstance(mantras, list):
            return result
        for i, m in enumerate(mantras):
            if not isinstance(m, dict):
                continue
            result.append(
                MantraDto(
                    id=f"{veda_name.lower()}_{i + 1}",
                    text=str(m.get("text", "")),
                    meaning=str(m.get("meaning", "")),
                    veda=veda_name,
                )
            )
    except Exception as e:
        logger.error("Error parsing %s Veda data: %s", veda_name, e)
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
        raise ResourceNotFoundError("Veda", veda_id)

    async def get_rig_veda_by_mandala(self, mandala: int, page: int, size: int) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_mandala(mandala)
        if api_list:
            all_v = [_map_rig_verse(x) for x in api_list]
        else:
            all_v = [RigVedaVerseDto.model_validate(x) for x in self._static.get_rig_veda_verses(mandala)]
        return paginate(all_v, page, size)

    async def get_rig_veda_by_deity(self, deity: str, page: int, size: int) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_deity(deity)
        all_v = [_map_rig_verse(x) for x in api_list] if api_list else []
        return paginate(all_v, page, size)

    async def get_rig_veda_by_poet(self, poet: str, page: int, size: int) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_poet(poet)
        all_v = [_map_rig_verse(x) for x in api_list] if api_list else []
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
            all_m = _parse_veda_mantras(raw, "Yajur")
        else:
            all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("yajur")]
        return paginate(all_m, page, size)

    async def get_sama_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._havyaka.get_mantras_by_name("sama", 500)
        if raw:
            all_m = [_map_havyaka_mantra(x) for x in raw]
        else:
            all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("sama")]
        return paginate(all_m, page, size)

    async def get_atharva_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._dharmic.get_atharva_veda()
        if raw:
            all_m = _parse_veda_mantras(raw, "Atharva")
        else:
            all_m = [MantraDto.model_validate(x) for x in self._static.get_veda_mantras("atharva")]
        return paginate(all_m, page, size)

    async def get_upanishads(self) -> List[UpanishadDto]:
        return [UpanishadDto.model_validate(x) for x in self._static.get_all_upanishads()]

    async def get_upanishad(self, upanishad_id: str) -> UpanishadDto:
        for u in self._static.get_all_upanishads():
            if str(u.get("id", "")).lower() == upanishad_id.lower():
                return UpanishadDto.model_validate(u)
        raise ResourceNotFoundError("Upanishad", upanishad_id)

    async def get_upanishad_verses(
        self, upanishad_id: str, chapter: int, page: int, size: int
    ) -> List[UpanishadVerseDto]:
        rows = self._static.get_upanishad_verses(upanishad_id, chapter)
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
        return [MantraDto.model_validate(x) for x in rows]
