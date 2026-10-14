from typing import List

from api.scriptures_api.ramayana_api.service_contract import RamayanaService
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import RamayanaKandaDto, RamayanaVerseDto
from services.static_registry import StaticContentRegistry


class DefaultRamayanaService(RamayanaService):
    def __init__(self, static: StaticContentRegistry) -> None:
        self.static = static

    async def get_ramayana_kandas(self) -> List[RamayanaKandaDto]:
        return [RamayanaKandaDto.model_validate(x) for x in self.static.get_ramayana_kandas()]

    async def get_ramayana_kanda(self, kanda_id: str) -> RamayanaKandaDto:
        wanted = kanda_id.strip().lower()
        for k in self.static.get_ramayana_kandas():
            if str(k.get("kandaId", "")).lower() == wanted:
                return RamayanaKandaDto.model_validate(k)
        raise ResourceNotFoundError("Ramayana kanda", kanda_id)

    async def get_ramayana_verses(
        self, kanda_id: str, sarga: int, skip: int, limit: int
    ) -> List[RamayanaVerseDto]:
        await self.get_ramayana_kanda(kanda_id)
        rows = self.static.get_ramayana_verses(kanda_id, sarga)
        page = 0 if not limit else skip // limit
        size = limit
        return paginate([RamayanaVerseDto.model_validate(x) for x in rows], page, size)

    async def get_ramayana_verse(self, kanda_id: str, sarga: int, verse: int) -> RamayanaVerseDto:
        await self.get_ramayana_kanda(kanda_id)
        for v in self.static.get_ramayana_verses(kanda_id, sarga):
            if int(v.get("verse") or 0) == verse:
                return RamayanaVerseDto.model_validate(v)
        raise ResourceNotFoundError("Ramayana verse", f"{kanda_id}:{sarga}:{verse}")
