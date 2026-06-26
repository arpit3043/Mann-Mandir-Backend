from typing import List, Optional, Protocol

from schemas.dtos import ChalisaDto

class ChalisaService(Protocol):
    async def get_chalisas(self, deity: Optional[str], page: int, size: int) -> List[ChalisaDto]: ...
    async def get_chalisa_by_id(self, chalisa_id: str) -> ChalisaDto: ...
