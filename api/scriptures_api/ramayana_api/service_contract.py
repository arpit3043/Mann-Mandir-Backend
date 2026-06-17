from abc import ABC, abstractmethod
from typing import List

from schemas.dtos import RamayanaKandaDto, RamayanaVerseDto


class RamayanaService(ABC):
    @abstractmethod
    async def get_ramayana_kandas(self) -> List[RamayanaKandaDto]:
        pass

    @abstractmethod
    async def get_ramayana_kanda(self, kanda_id: str) -> RamayanaKandaDto:
        pass

    @abstractmethod
    async def get_ramayana_verses(self, kanda_id: str, sarga: int, skip: int, limit: int) -> List[RamayanaVerseDto]:
        pass

    @abstractmethod
    async def get_ramayana_verse(self, kanda_id: str, sarga: int, verse: int) -> RamayanaVerseDto:
        pass
