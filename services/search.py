from __future__ import annotations

from typing import List, Optional

from core.content_domain import ContentDomain, parse_content_domain
from core.pagination import JAVA_MAX_INT
from schemas.dtos import SearchResultDto
from services.contracts import GodService, ScriptureService, VedaService


class DefaultSearchService:
    def __init__(
        self,
        god: GodService,
        scripture: ScriptureService,
        veda: VedaService,
    ) -> None:
        self._god = god
        self._scripture = scripture
        self._veda = veda

    async def search(
        self, query: str, domain: Optional[str], page: int, size: int
    ) -> List[SearchResultDto]:
        q = query.lower().strip()
        content_domain = parse_content_domain(domain)
        combined: List[SearchResultDto] = []

        if content_domain is None or content_domain == ContentDomain.GOD:
            combined.extend(await self._search_aartis(q))
            combined.extend(await self._search_chalisas(q))
            combined.extend(await self._search_stotrams(q))

        if content_domain is None or content_domain == ContentDomain.SCRIPTURES:
            combined.extend(await self._search_gita(q))

        if content_domain is None or content_domain == ContentDomain.VEDAS:
            combined.extend(await self._search_vedas(q))

        combined.sort(key=lambda r: r.relevanceScore, reverse=True)
        start = page * size
        end = start + size
        return combined[start:end]

    async def count(self, query: str, domain: Optional[str]) -> int:
        all_rows = await self.search(query, domain, 0, JAVA_MAX_INT)
        return len(all_rows)

    async def _search_aartis(self, q: str) -> List[SearchResultDto]:
        rows = await self._god.get_aartis(None, 0, 100)
        out: List[SearchResultDto] = []
        for a in rows:
            if self._matches(q, a.name, a.deity):
                out.append(
                    SearchResultDto(
                        id=a.id,
                        type="AARTI",
                        source="GOD",
                        title=a.name,
                        snippet=self._truncate(a.translation or "", 120),
                        relevanceScore=self._score(q, a.name, a.deity),
                        metadata={"deity": a.deity},
                    )
                )
        return out

    async def _search_chalisas(self, q: str) -> List[SearchResultDto]:
        rows = await self._god.get_chalisas(0, 50)
        out: List[SearchResultDto] = []
        for c in rows:
            if self._matches(q, c.title, c.deity):
                out.append(
                    SearchResultDto(
                        id=c.id,
                        type="CHALISA",
                        source="GOD",
                        title=c.title,
                        snippet=f"{c.deity} Chalisa — {c.totalVerses} verses",
                        relevanceScore=self._score(q, c.title, c.deity),
                        metadata={"deity": c.deity, "verses": c.totalVerses},
                    )
                )
        return out

    async def _search_stotrams(self, q: str) -> List[SearchResultDto]:
        rows = await self._god.get_stotrams(None, 0, 100)
        out: List[SearchResultDto] = []
        for s in rows:
            if self._matches(q, s.name, s.deity, s.description):
                author = s.author or ""
                out.append(
                    SearchResultDto(
                        id=s.id,
                        type="STOTRAM",
                        source="GOD",
                        title=s.name,
                        snippet=self._truncate(s.description or "", 120),
                        relevanceScore=self._score(q, s.name, s.deity),
                        metadata={"deity": s.deity, "author": author},
                    )
                )
        return out

    async def _search_gita(self, q: str) -> List[SearchResultDto]:
        chapters = await self._scripture.get_gita_chapters()
        out: List[SearchResultDto] = []
        for c in chapters:
            if self._matches(q, c.name, c.translation, c.summary):
                out.append(
                    SearchResultDto(
                        id=f"gita_ch_{c.number}",
                        type="CHAPTER",
                        source="BHAGAVAD_GITA",
                        title=f"Chapter {c.number} — {c.translation}",
                        snippet=self._truncate(c.summary or "", 120),
                        relevanceScore=self._score(q, c.name, c.translation),
                        metadata={"chapter": c.number, "verses": c.versesCount},
                    )
                )
        return out

    async def _search_vedas(self, q: str) -> List[SearchResultDto]:
        vedas = await self._veda.get_all_vedas()
        out: List[SearchResultDto] = []
        for v in vedas:
            if self._matches(q, v.name, v.description):
                out.append(
                    SearchResultDto(
                        id=v.vedaId,
                        type="VEDA",
                        source="VEDA",
                        title=v.name,
                        snippet=self._truncate(v.description or "", 120),
                        relevanceScore=self._score(q, v.name, v.description),
                        metadata={"hymns": v.hymns, "verses": v.verses},
                    )
                )
        return out

    def _matches(self, query: str, *fields: Optional[str]) -> bool:
        for f in fields:
            if f and query in f.lower():
                return True
        return False

    def _score(self, query: str, *fields: Optional[str]) -> float:
        best = 0.0
        for f in fields:
            if not f:
                continue
            lower = f.lower()
            if lower == query:
                best = max(best, 1.0)
            elif lower.startswith(query):
                best = max(best, 0.9)
            elif query in lower:
                best = max(best, 0.7)
        return best

    def _truncate(self, text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        return text[:max_len] + "…"
