from typing import List, Optional, Protocol

from schemas.dtos import (
    MantraDto,
    RigVedaVerseDto,
    SearchResultDto,
    UpanishadDto,
    UpanishadVerseDto,
    VedaDto,
)


class SearchService(Protocol):
    async def search(
            self,
            query: str,
            domain: Optional[str],
            page: int,
            size: int,
            content_type: Optional[str] = None,
    ) -> List[SearchResultDto]:
        pass

    async def count(
            self, query: str, domain: Optional[str], content_type: Optional[str] = None
    ) -> int:
        pass


class VedaService(Protocol):
    async def get_all_vedas(self) -> List[VedaDto]:
        pass

    async def get_veda(self, veda_id: str) -> VedaDto:
        pass

    async def get_rig_veda_by_mandala(
            self, mandala: int, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        pass

    async def get_rig_veda_by_deity(
            self, deity: str, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        pass

    async def get_rig_veda_by_poet(
            self, poet: str, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        pass

    async def get_rig_veda_verse(
            self, mandala: int, sukta: int, stanza: int
    ) -> RigVedaVerseDto:
        pass

    async def get_yajur_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        pass

    async def get_sama_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        pass

    async def get_atharva_veda_mantras(
            self, page: int, size: int
    ) -> List[MantraDto]:
        pass

    async def get_upanishads(self) -> List[UpanishadDto]:
        pass

    async def get_upanishad(self, upanishad_id: str) -> UpanishadDto:
        pass

    async def get_upanishad_verses(
            self,
            upanishad_id: str,
            chapter: Optional[int],
            page: int,
            size: int,
    ) -> List[UpanishadVerseDto]:
        pass

    async def get_upanishad_verse(
            self, upanishad_id: str, chapter: int, verse: int
    ) -> UpanishadVerseDto:
        pass

    async def get_random_vedic_mantra(self) -> MantraDto:
        pass

    async def search_mantras(self, deity: str, limit: int) -> List[MantraDto]:
        pass
