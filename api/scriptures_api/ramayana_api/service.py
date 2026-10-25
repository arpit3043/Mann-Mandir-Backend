from typing import List

from api.scriptures_api.ramayana_api.service_contract import RamayanaService
from clients.upstream import DharmicDataClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import suggestion_for
from schemas.dtos import RamayanaKandaDto, RamayanaVerseDto
from services.static_registry import StaticContentRegistry


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class DefaultRamayanaService(RamayanaService):
    def __init__(
            self, dharmic: DharmicDataClient, static: StaticContentRegistry
    ) -> None:
        self._dharmic = dharmic
        self.static = static

    async def get_ramayana_kandas(self) -> List[RamayanaKandaDto]:
        return [
            RamayanaKandaDto.model_validate(x)
            for x in self.static.get_ramayana_kandas()
        ]

    async def get_ramayana_kanda(self, kanda_id: str) -> RamayanaKandaDto:
        wanted = kanda_id.strip().lower()
        for k in self.static.get_ramayana_kandas():
            if str(k.get("kandaId", "")).lower() == wanted:
                return RamayanaKandaDto.model_validate(k)
        names = [str(k.get("kandaId") or "") for k in self.static.get_ramayana_kandas()]
        raise ResourceNotFoundError(
            "Ramayana kanda", kanda_id, suggestion=suggestion_for(kanda_id, names)
        )

    async def _verses_for_sarga(
            self, kanda_id: str, sarga: int
    ) -> List[RamayanaVerseDto]:
        await self.get_ramayana_kanda(kanda_id)
        raw = await self._dharmic.get_ramayana_kanda(kanda_id)
        if raw:
            out: List[RamayanaVerseDto] = []
            for item in raw:
                if (
                        _as_int(
                            item.get("sarg")
                            if item.get("sarg") is not None
                            else item.get("sarga")
                        )
                        != sarga
                ):
                    continue
                out.append(
                    RamayanaVerseDto(
                        kandaId=kanda_id.strip().lower(),
                        sarga=sarga,
                        verse=_as_int(
                            item.get("shloka")
                            if item.get("shloka") is not None
                            else item.get("verse")
                        ),
                        original=str(item.get("text") or item.get("original") or "")
                                 or None,
                        transliteration=str(item.get("transliteration") or "") or None,
                        translation=str(item.get("translation") or "") or None,
                    )
                )
            if out:
                return out
        return [
            RamayanaVerseDto.model_validate(x)
            for x in self.static.get_ramayana_verses(kanda_id, sarga)
        ]

    async def get_ramayana_verses(
            self, kanda_id: str, sarga: int, skip: int, limit: int
    ) -> List[RamayanaVerseDto]:
        rows = await self._verses_for_sarga(kanda_id, sarga)
        if not rows:
            raise ResourceNotFoundError(
                "Ramayana sarga",
                f"{kanda_id}/{sarga}",
                suggestion="Try searching: bala/1",
            )
        page = 0 if not limit else skip // limit
        size = limit
        return paginate(rows, page, size)

    async def get_ramayana_verse(
            self, kanda_id: str, sarga: int, verse: int
    ) -> RamayanaVerseDto:
        for v in await self._verses_for_sarga(kanda_id, sarga):
            if v.verse == verse:
                return v
        raise ResourceNotFoundError("Ramayana verse", f"{kanda_id}:{sarga}:{verse}")
