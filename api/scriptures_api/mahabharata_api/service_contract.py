from typing import List, Protocol

from schemas.dtos import MahabharataParvaDto, MahabharataVerseDto


class MahabharataService(Protocol):
    async def get_mahabharata_parvas(self) -> List[MahabharataParvaDto]:
        pass

    async def get_mahabharata_parva(self, parva_number: int) -> MahabharataParvaDto:
        pass

    async def get_mahabharata_verses(
            self, parva_number: int, chapter_number: int, page: int, size: int
    ) -> List[MahabharataVerseDto]:
        pass

    async def get_mahabharata_verse(
            self, parva_number: int, chapter_number: int, verse: int
    ) -> MahabharataVerseDto:
        pass
