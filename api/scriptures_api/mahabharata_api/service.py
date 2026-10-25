from typing import List

from api.scriptures_api.mahabharata_api.service_contract import MahabharataService
from clients.upstream import DharmicDataClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import suggestion_for
from schemas.dtos import MahabharataParvaDto, MahabharataVerseDto
from services.static_registry import StaticContentRegistry


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class DefaultMahabharataService(MahabharataService):
    def __init__(self, dharmic: DharmicDataClient, static: StaticContentRegistry) -> None:
        self._dharmic = dharmic
        self._static = static

    async def get_mahabharata_parvas(self) -> List[MahabharataParvaDto]:
        parvas = self._static.get_mahabharata_parvas()
        return [MahabharataParvaDto.model_validate(x) for x in parvas]

    async def get_mahabharata_parva(self, parva_number: int) -> MahabharataParvaDto:
        for p in self._static.get_mahabharata_parvas():
            number = p.get("parvaNumber", p.get("id"))
            try:
                if int(number) == parva_number:
                    return MahabharataParvaDto.model_validate(p)
            except (TypeError, ValueError):
                continue
        names = [str(p.get("parvaNumber") or p.get("name") or "") for p in self._static.get_mahabharata_parvas()]
        raise ResourceNotFoundError(
            "Mahabharata parva",
            str(parva_number),
            suggestion=suggestion_for(str(parva_number), names, fallback="Try searching: 1"),
        )

    async def _verses_for_chapter(self, parva_number: int, chapter_number: int) -> List[MahabharataVerseDto]:
        await self.get_mahabharata_parva(parva_number)
        raw = await self._dharmic.get_mahabharata_parva(parva_number)
        if raw:
            out: List[MahabharataVerseDto] = []
            for item in raw:
                if _as_int(item.get("chapter")) != chapter_number:
                    continue
                out.append(
                    MahabharataVerseDto(
                        parva=_as_int(item.get("book"), parva_number),
                        chapter=chapter_number,
                        verse=_as_int(item.get("shloka") if item.get("shloka") is not None else item.get("verse")),
                        text=str(item.get("text") or "") or None,
                        translation=str(item.get("translation") or "") or None,
                    )
                )
            if out:
                return out
        return [
            MahabharataVerseDto.model_validate(x)
            for x in self._static.get_mahabharata_verses(parva_number, chapter_number)
        ]

    async def get_mahabharata_verses(
        self, parva_number: int, chapter_number: int, page: int, size: int
    ) -> List[MahabharataVerseDto]:
        all_verses = await self._verses_for_chapter(parva_number, chapter_number)
        if not all_verses:
            raise ResourceNotFoundError(
                "Mahabharata chapter",
                f"{parva_number}/{chapter_number}",
                suggestion="Try searching: 1/1",
            )
        return paginate(all_verses, page, size)

    async def get_mahabharata_verse(
        self, parva_number: int, chapter_number: int, verse: int
    ) -> MahabharataVerseDto:
        for v in await self._verses_for_chapter(parva_number, chapter_number):
            if v.verse == verse:
                return v
        raise ResourceNotFoundError("Mahabharata verse", f"{parva_number}.{chapter_number}.{verse}")
