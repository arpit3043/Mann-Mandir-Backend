from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from api.aarti_api.service_contract import AartiService
from api.chalisa_api.service_contract import ChalisaService
from api.mantra_api.service_contract import MantraService
from api.scriptures_api.gita_api.service_contract import GitaService
from api.stotram_api.service_contract import StotramService
from core.content_domain import ContentDomain, parse_content_domain
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import compact, expand_term, suggestion_for
from schemas.dtos import SearchResultDto
from services.contracts import SearchService, VedaService
from services.static_registry import CHALISA_VERSES

_TOKEN_RE = re.compile(r"[a-z0-9]+|[\u0900-\u097f]+", re.IGNORECASE)

_TYPE_WORDS = {
    "aarti": "aarti",
    "aartis": "aarti",
    "arti": "aarti",
    "aarties": "aarti",
    "आरती": "aarti",
    "chalisa": "chalisa",
    "chalisas": "chalisa",
    "chaleesa": "chalisa",
    "चालीसा": "chalisa",
    "stotram": "stotram",
    "stotra": "stotram",
    "stotrams": "stotram",
    "स्तोत्र": "stotram",
    "स्तोत्रम्": "stotram",
    "mantra": "mantra",
    "mantras": "mantra",
    "मंत्र": "mantra",
    "मन्त्र": "mantra",
    "gita": "gita",
    "geeta": "gita",
    "गीता": "gita",
    "veda": "veda",
    "vedas": "veda",
    "वेद": "veda",
    "upanishad": "upanishad",
    "upanishads": "upanishad",
    "उपनिषद": "upanishad",
}

_VALID_TYPES = {"aarti", "chalisa", "stotram", "mantra", "gita", "veda", "upanishad"}


@dataclass
class _Doc:
    id: str
    type: str
    source: str
    title: str
    snippet: str = ""
    deity: str = ""
    body: str = ""
    fields: Dict[str, str] = field(default_factory=dict)


def _tokens(text: str) -> List[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text or "") if token]


def _parse_types(value: Optional[str]) -> Set[str]:
    if not value or not str(value).strip():
        return set()
    types: Set[str] = set()
    for part in re.split(r"[,\s]+", str(value).strip().lower()):
        if not part:
            continue
        mapped = _TYPE_WORDS.get(part, part)
        if mapped not in _VALID_TYPES:
            raise ValueError("Unknown type. Try aarti, chalisa, stotram or mantra")
        types.add(mapped)
    return types


def _parse_query(query: str) -> Tuple[List[str], Set[str]]:
    types: Set[str] = set()
    terms: List[str] = []
    seen: Set[str] = set()
    for raw in _tokens(query):
        mapped_type = _TYPE_WORDS.get(raw)
        if mapped_type:
            types.add(mapped_type)
            continue
        for term in expand_term(raw):
            if term not in seen:
                seen.add(term)
                terms.append(term)
    return terms, types


def _join(parts: Iterable[Optional[str]]) -> str:
    return " ".join(part.strip() for part in parts if part and str(part).strip())


def _chalisa_lyrics(chalisa_id: str) -> str:
    parts: List[str] = []
    for verse in CHALISA_VERSES.get(chalisa_id, []):
        parts.extend(
            [
                str(verse.get("devanagari") or ""),
                str(verse.get("transliteration") or ""),
                str(verse.get("englishTranslation") or ""),
            ]
        )
    return _join(parts)


def _field_hit(term: str, value: str) -> float:
    if not term or not value:
        return 0.0
    compact_term = compact(term)
    compact_value = compact(value)
    value_tokens = _tokens(value)
    if compact_term == compact_value:
        return 1.0
    if compact_value.startswith(compact_term) or compact_term.startswith(compact_value):
        return 0.9
    if compact_term in compact_value:
        return 0.75
    for word in value_tokens:
        compact_word = compact(word)
        if compact_word.startswith(compact_term) or compact_term.startswith(
            compact_word
        ):
            return 0.7
        if (
            len(compact_term) >= 3
            and SequenceMatcher(None, compact_term, compact_word).ratio() >= 0.78
        ):
            return 0.55
    return 0.0


def _score(doc: _Doc, terms: Sequence[str], types: Set[str]) -> float:
    if types and doc.type not in types:
        return 0.0
    if not terms:
        return 4.0 if types else 0.0

    unique_terms = list(dict.fromkeys(terms))
    if types:
        identity_hit = any(
            _field_hit(term, doc.deity)
            or _field_hit(term, doc.title)
            or _field_hit(term, doc.id)
            for term in unique_terms
        )
        if not identity_hit:
            return 0.0
    matched = 0
    score = 0.0
    for term in unique_terms:
        best = 0.0
        best += 12.0 * _field_hit(term, doc.deity)
        best += 9.0 * _field_hit(term, doc.title)
        best += 7.0 * _field_hit(term, doc.id)
        best += 5.0 * _field_hit(term, doc.type)
        best += 3.0 * _field_hit(term, doc.snippet)
        best += 2.0 * _field_hit(term, doc.body)
        if best > 0:
            matched += 1
            score += best
    if matched == 0:
        return 0.0
    coverage = matched / max(len(unique_terms), 1)
    if coverage < 0.5:
        return 0.0
    if types:
        score += 5.0
    return score * (0.6 + 0.4 * coverage)


def _to_result(doc: _Doc, score: float) -> SearchResultDto:
    snippet = doc.snippet
    if not snippet and doc.body:
        snippet = doc.body[:180].strip()
    return SearchResultDto(
        id=doc.id,
        type=doc.type,
        source=doc.source,
        title=doc.title,
        snippet=snippet,
        relevanceScore=round(score, 3),
        metadata={"deity": doc.deity} if doc.deity else None,
    )


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
        self,
        query: str,
        domain: Optional[str],
        page: int,
        size: int,
        content_type: Optional[str] = None,
    ) -> List[SearchResultDto]:
        results = await self._collect(query, domain, content_type)
        return paginate(results, page, size)

    async def count(
        self, query: str, domain: Optional[str], content_type: Optional[str] = None
    ) -> int:
        return len(await self._collect(query, domain, content_type))

    async def _collect(
        self, query: str, domain: Optional[str], content_type: Optional[str] = None
    ) -> List[SearchResultDto]:
        parsed = parse_content_domain(domain)
        terms, types = _parse_query(query)
        types |= _parse_types(content_type)
        if not terms and not types:
            raise ResourceNotFoundError(
                "Search",
                query or "requested data",
                suggestion="Try searching: shiva, hanuman chalisa or lakshmi aarti",
            )

        include_god = parsed is None or parsed == ContentDomain.GOD
        include_scriptures = parsed is None or parsed == ContentDomain.SCRIPTURES
        include_vedas = parsed is None or parsed == ContentDomain.VEDAS
        docs: List[_Doc] = []

        if include_god:
            docs.extend(await self._god_docs())
        if include_scriptures:
            docs.extend(await self._scripture_docs())
        if include_vedas:
            docs.extend(await self._veda_docs())

        ranked: List[Tuple[float, _Doc]] = []
        seen: Set[Tuple[str, str]] = set()
        for doc in docs:
            key = (doc.type, doc.id)
            if key in seen:
                continue
            seen.add(key)
            score = _score(doc, terms, types)
            if score > 0:
                ranked.append((score, doc))
        ranked.sort(key=lambda item: (-item[0], item[1].title.lower()))
        if not ranked:
            available = []
            for doc in docs:
                if doc.deity:
                    available.append(doc.deity)
                if doc.title:
                    available.append(doc.title)
            raise ResourceNotFoundError(
                "Search",
                query or "requested data",
                suggestion=suggestion_for(
                    query,
                    available,
                    fallback="Try searching: shiva, hanuman chalisa or lakshmi aarti",
                ),
            )
        return [_to_result(doc, score) for score, doc in ranked]

    async def _god_docs(self) -> List[_Doc]:
        docs: List[_Doc] = []
        try:
            for aarti in await self.aarti.get_aartis(None, 0, 1000):
                verses = aarti.verses or []
                body = _join(
                    [
                        aarti.devanagari,
                        aarti.transliteration,
                        aarti.translation,
                        *verses,
                    ]
                )
                docs.append(
                    _Doc(
                        id=aarti.id,
                        type="aarti",
                        source="local",
                        title=aarti.name,
                        snippet=aarti.translation or aarti.transliteration or "",
                        deity=aarti.deity,
                        body=body,
                    )
                )
        except Exception:
            pass

        try:
            for chalisa in await self.chalisa.get_chalisas(None, 0, 1000):
                docs.append(
                    _Doc(
                        id=chalisa.id,
                        type="chalisa",
                        source="local",
                        title=chalisa.title,
                        snippet=f"{chalisa.deity} Chalisa",
                        deity=chalisa.deity,
                        body=_chalisa_lyrics(chalisa.id),
                    )
                )
        except Exception:
            pass

        try:
            for stotram in await self.stotram.get_stotrams(None, 0, 1000):
                docs.append(
                    _Doc(
                        id=stotram.id,
                        type="stotram",
                        source="local",
                        title=stotram.name,
                        snippet=stotram.description or "",
                        deity=stotram.deity,
                        body=_join(
                            [
                                stotram.name,
                                stotram.deity,
                                stotram.description,
                                stotram.author,
                            ]
                        ),
                    )
                )
        except Exception:
            pass

        try:
            for mantra in await self.mantra.get_mantras(None, 0, 1000):
                docs.append(
                    _Doc(
                        id=mantra.id or mantra.name or "mantra",
                        type="mantra",
                        source="local",
                        title=mantra.name or mantra.text or "Mantra",
                        snippet=mantra.meaning or "",
                        deity=mantra.deity or "",
                        body=_join(
                            [
                                mantra.name,
                                mantra.deity,
                                mantra.text,
                                mantra.devanagari,
                                mantra.transliteration,
                                mantra.meaning,
                                " ".join(mantra.tags or []),
                            ]
                        ),
                    )
                )
        except Exception:
            pass
        return docs

    async def _scripture_docs(self) -> List[_Doc]:
        docs: List[_Doc] = []
        try:
            for chapter in await self.gita.get_gita_chapters():
                docs.append(
                    _Doc(
                        id=f"gita-chapter-{chapter.number}",
                        type="gita",
                        source="gita",
                        title=chapter.translation or chapter.name,
                        snippet=chapter.summary or "",
                        body=_join(
                            [
                                chapter.name,
                                chapter.translation,
                                chapter.transliteration,
                                chapter.summary,
                            ]
                        ),
                    )
                )
        except Exception:
            pass
        return docs

    async def _veda_docs(self) -> List[_Doc]:
        docs: List[_Doc] = []
        try:
            for veda in await self.veda.get_all_vedas():
                docs.append(
                    _Doc(
                        id=veda.vedaId,
                        type="veda",
                        source="local",
                        title=veda.name,
                        snippet=veda.description or "",
                        body=_join([veda.vedaId, veda.name, veda.description]),
                    )
                )
        except Exception:
            pass
        try:
            for upanishad in await self.veda.get_upanishads():
                docs.append(
                    _Doc(
                        id=upanishad.id,
                        type="upanishad",
                        source="local",
                        title=upanishad.name,
                        snippet=upanishad.description or "",
                        body=_join(
                            [upanishad.id, upanishad.name, upanishad.description]
                        ),
                    )
                )
        except Exception:
            pass
        return docs
