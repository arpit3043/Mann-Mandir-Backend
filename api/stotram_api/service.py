from typing import List, Optional

from api.stotram_api.service_contract import StotramService
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import StotramDto
from services.static_registry import StaticContentRegistry


class DefaultStotramService(StotramService):
    def __init__(self, static: StaticContentRegistry) -> None:
        self.static = static

    async def get_stotrams(self, deity: Optional[str], page: int, size: int) -> List[StotramDto]:
        all_rows = self.static.get_all_stotrams()
        if deity and deity.strip():
            d = deity.strip().lower()
            all_rows = [s for s in all_rows if str(s.get("deity", "")).lower() == d]
        page_rows = paginate(all_rows, page, size)
        return [StotramDto.model_validate(x) for x in page_rows]

    async def get_stotram_by_id(self, stotram_id: str) -> StotramDto:
        for s in self.static.get_all_stotrams():
            if s.get("id") == stotram_id:
                return StotramDto.model_validate(s)
        raise ResourceNotFoundError("Stotram", stotram_id)
