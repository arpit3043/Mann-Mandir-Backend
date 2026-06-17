from typing import List, Optional

from api.aarti_api.service_contract import AartiService
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import AartiDto
from services.static_registry import StaticContentRegistry


class DefaultAartiService(AartiService):
    def __init__(self, static: StaticContentRegistry) -> None:
        self._static = static

    async def get_aartis(self, deity: Optional[str], page: int, size: int) -> List[AartiDto]:
        all_rows = self._static.get_all_aartis()
        if deity and deity.strip():
            d = deity.strip().lower()
            all_rows = [a for a in all_rows if str(a.get("deity", "")).lower() == d]
        page_rows = paginate(all_rows, page, size)
        return [AartiDto.model_validate(x) for x in page_rows]

    async def get_aarti_by_id(self, aarti_id: str) -> AartiDto:
        for a in self._static.get_all_aartis():
            if a.get("id") == aarti_id:
                return AartiDto.model_validate(a)
        raise ResourceNotFoundError("Aarti", aarti_id)

    async def get_aarti_deities(self) -> List[str]:
        return sorted({str(a["deity"]) for a in self._static.get_all_aartis() if a.get("deity")})
