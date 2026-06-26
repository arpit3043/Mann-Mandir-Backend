from typing import List

from api.scriptures_api.mahabharata_api.service_contract import MahabharataService
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from schemas.dtos import MahabharataParvaDto, MahabharataVerseDto
from services.static_registry import StaticContentRegistry


class DefaultMahabharataService(MahabharataService):
    def __init__(self, static: StaticContentRegistry) -> None:
        self._static = static

    async def get_mahabharata_parvas(self) -> List[MahabharataParvaDto]:
        parvas = self._static.get_mahabharata_parvas()
        return [MahabharataParvaDto.model_validate(x) for x in parvas]

    async def get_mahabharata_parva(self, parva_number: int) -> MahabharataParvaDto:
        for p in self._static.get_mahabharata_parvas():
            if p.get("id") == parva_number:
                return MahabharataParvaDto.model_validate(p)
        raise ResourceNotFoundError("Mahabharata parva", str(parva_number))

    async def get_mahabharata_verses(
        self, parva_number: int, chapter_number: int, page: int, size: int
    ) -> List[MahabharataVerseDto]:
        all_verses = self._static.get_mahabharata_verses(parva_number, chapter_number)
        if not all_verses:
            return []
        page_verses = paginate(all_verses, page, size)
        return [MahabharataVerseDto.model_validate(x) for x in page_verses]

    async def get_mahabharata_verse(
        self, parva_number: int, chapter_number: int, verse: int
    ) -> MahabharataVerseDto:
        all_verses = self._static.get_mahabharata_verses(parva_number, chapter_number)
        for v in all_verses:
            if v.get("verse") == verse:
                return MahabharataVerseDto.model_validate(v)
        raise ResourceNotFoundError("Mahabharata verse", f"{parva_number}.{chapter_number}.{verse}")
