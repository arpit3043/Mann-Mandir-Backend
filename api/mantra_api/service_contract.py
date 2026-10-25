from typing import List, Optional, Protocol

from schemas.dtos import MantraDto


class MantraService(Protocol):
    async def get_mantras(
            self, deity: Optional[str], page: int, size: int
    ) -> List[MantraDto]:
        pass

    async def get_random_mantra(self, date: Optional[str] = None) -> MantraDto:
        pass
