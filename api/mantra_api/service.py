from typing import List, Optional

from api.mantra_api.service_contract import MantraService
from clients.upstream import HavyakaApiClient, ShlokaApiClient
from core.pagination import paginate
from schemas.dtos import MantraDto
from services.static_registry import StaticContentRegistry


class DefaultMantraService(MantraService):
    def __init__(
        self, havyaka: HavyakaApiClient, shloka: ShlokaApiClient, static: StaticContentRegistry
    ) -> None:
        self.havyaka = havyaka
        self.shloka = shloka
        self.static = static

    async def get_mantras(self, deity: Optional[str], page: int, size: int) -> List[MantraDto]:
        all_rows = self.static.get_mantras(deity, limit=9999)
        page_rows = paginate(all_rows, page, size)
        return [MantraDto.model_validate(x) for x in page_rows]

    async def get_random_mantra(self) -> MantraDto:
        # Check upstream first
        random_up = await self.shloka.get_random_shloka()
        if random_up:
            return MantraDto(
                text=str(random_up.get("slogan", "")),
                meaning=str(random_up.get("meaning", ""))
            )
        # Fallback to static
        random_static = self.static.get_random_mantra()
        return MantraDto.model_validate(random_static)
