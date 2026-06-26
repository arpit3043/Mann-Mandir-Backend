from typing import List
from schemas.dtos import RamayanaKandaDto, RamayanaVerseDto
from api.scriptures_api.ramayana_api.service_contract import RamayanaService
from core.exceptions import ResourceNotFoundError

class DefaultRamayanaService(RamayanaService):
    def __init__(self, static):
        self.static = static

    async def get_ramayana_kandas(self) -> List[RamayanaKandaDto]:
        return []

    async def get_ramayana_kanda(self, kanda_id: str) -> RamayanaKandaDto:
        raise ResourceNotFoundError("Ramayana kanda", kanda_id)

    async def get_ramayana_verses(self, kanda_id: str, sarga: int, skip: int, limit: int) -> List[RamayanaVerseDto]:
        return []

    async def get_ramayana_verse(self, kanda_id: str, sarga: int, verse: int) -> RamayanaVerseDto:
        raise ResourceNotFoundError("Ramayana verse", f"{kanda_id}:{sarga}:{verse}")
