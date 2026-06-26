from typing import List, Optional

from api.chalisa_api.service_contract import ChalisaService
from clients.upstream import HanumanChalisaClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import ChalisaDto, ChalisaVerseDto
from services.static_registry import StaticContentRegistry


class DefaultChalisaService(ChalisaService):
    def __init__(self, hanuman: HanumanChalisaClient, static: StaticContentRegistry) -> None:
        self.hanuman = hanuman
        self.static = static

    async def get_chalisas(self, deity: Optional[str], page: int, size: int) -> List[ChalisaDto]:
        all_rows = self.static.get_all_chalisas()
        if deity and deity.strip():
            d = deity.strip().lower()
            all_rows = [c for c in all_rows if str(c.get("deity", "")).lower() == d]
        page_rows = paginate(all_rows, page, size)
        return [ChalisaDto.model_validate(x) for x in page_rows]

    async def get_chalisa_by_id(self, chalisa_id: str) -> ChalisaDto:
        for c in self.static.get_all_chalisas():
            if c.get("id") == chalisa_id:
                dto = ChalisaDto.model_validate(c)
                # If Hanuman chalisa, fetch verses from upstream
                if chalisa_id == "chalisa-hanuman":
                    verses = await self.hanuman.get_all_verses()
                    if verses:
                        dto.verses = [ChalisaVerseDto.model_validate(v) for v in verses]
                return dto
        raise ResourceNotFoundError("Chalisa", chalisa_id)
