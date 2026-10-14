from typing import List, Optional

from api.aarti_api.service_contract import AartiService
from api.chalisa_api.service_contract import ChalisaService
from api.mantra_api.service_contract import MantraService
from api.scriptures_api.gita_api.service_contract import GitaService
from api.stotram_api.service_contract import StotramService
from core.content_domain import ContentDomain, parse_content_domain
from core.pagination import paginate
from schemas.dtos import SearchResultDto
from services.contracts import SearchService, VedaService


class DefaultSearchService(SearchService):
    def __init__(
        self,
        aarti: AartiService,
        chalisa: ChalisaService,
        stotram: StotramService,
        mantra: MantraService,
        gita: GitaService,
        veda: VedaService,
    ) -> None:
        self.aarti = aarti
        self.chalisa = chalisa
        self.stotram = stotram
        self.mantra = mantra
        self.gita = gita
        self.veda = veda

    async def search(
        self, query: str, domain: Optional[str], page: int, size: int
    ) -> List[SearchResultDto]:
        results = await self._collect(query, domain)
        return paginate(results, page, size)

    async def count(self, query: str, domain: Optional[str]) -> int:
        return len(await self._collect(query, domain))

    async def _collect(self, query: str, domain: Optional[str]) -> List[SearchResultDto]:
        parsed = parse_content_domain(domain)
        q = (query or "").strip().lower()
        if not q:
            return []

        include_god = parsed is None or parsed == ContentDomain.GOD
        include_scriptures = parsed is None or parsed == ContentDomain.SCRIPTURES
        include_vedas = parsed is None or parsed == ContentDomain.VEDAS
        results: List[SearchResultDto] = []

        if include_god:
            results.extend(await self._search_god(q))
        if include_scriptures:
            results.extend(await self._search_scriptures(q))
        if include_vedas:
            results.extend(await self._search_vedas(q))
        return results

    async def _search_god(self, q: str) -> List[SearchResultDto]:
        results: List[SearchResultDto] = []
        try:
            aartis = await self.aarti.get_aartis(None, 0, 1000)
            for a in aartis:
                haystack = " ".join(filter(None, [a.name, a.deity, a.translation]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(
                            id=a.id,
                            type="aarti",
                            source="local",
                            title=a.name,
                            snippet=a.translation or "",
                        )
                    )
        except Exception:
            pass

        try:
            chalisas = await self.chalisa.get_chalisas(None, 0, 1000)
            for c in chalisas:
                haystack = " ".join(filter(None, [c.title, c.deity, c.id]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(id=c.id, type="chalisa", source="local", title=c.title)
                    )
        except Exception:
            pass

        try:
            stotrams = await self.stotram.get_stotrams(None, 0, 1000)
            for s in stotrams:
                haystack = " ".join(filter(None, [s.name, s.deity, s.description]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(id=s.id, type="stotram", source="local", title=s.name)
                    )
        except Exception:
            pass

        try:
            mantras = await self.mantra.get_mantras(None, 0, 1000)
            for m in mantras:
                haystack = " ".join(filter(None, [m.name, m.deity, m.meaning, m.text]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(
                            id=m.id or m.name or "mantra",
                            type="mantra",
                            source="local",
                            title=m.name or m.text or "Mantra",
                            snippet=m.meaning or "",
                        )
                    )
        except Exception:
            pass
        return results

    async def _search_scriptures(self, q: str) -> List[SearchResultDto]:
        results: List[SearchResultDto] = []
        try:
            chapters = await self.gita.get_gita_chapters()
            for ch in chapters:
                haystack = " ".join(
                    filter(None, [ch.name, ch.translation, ch.transliteration, ch.summary])
                )
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(
                            id=f"gita-chapter-{ch.number}",
                            type="gita",
                            source="gita",
                            title=ch.translation or ch.name,
                            snippet=ch.summary or "",
                        )
                    )
        except Exception:
            pass
        return results

    async def _search_vedas(self, q: str) -> List[SearchResultDto]:
        results: List[SearchResultDto] = []
        try:
            vedas = await self.veda.get_all_vedas()
            for v in vedas:
                haystack = " ".join(filter(None, [v.vedaId, v.name, v.description]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(
                            id=v.vedaId,
                            type="veda",
                            source="local",
                            title=v.name,
                            snippet=v.description or "",
                        )
                    )
        except Exception:
            pass

        try:
            upanishads = await self.veda.get_upanishads()
            for u in upanishads:
                haystack = " ".join(filter(None, [u.id, u.name, u.description]))
                if q in haystack.lower():
                    results.append(
                        SearchResultDto(
                            id=u.id,
                            type="upanishad",
                            source="local",
                            title=u.name,
                            snippet=u.description or "",
                        )
                    )
        except Exception:
            pass
        return results
