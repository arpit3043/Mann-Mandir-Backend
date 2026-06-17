from typing import List, Optional, Protocol

from schemas.dtos import StotramDto

class StotramService(Protocol):
    async def get_stotrams(self, deity: Optional[str], page: int, size: int) -> List[StotramDto]: ...
    async def get_stotram_by_id(self, stotram_id: str) -> StotramDto: ...
