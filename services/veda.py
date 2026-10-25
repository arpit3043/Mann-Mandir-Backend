from __future__ import annotations

import asyncio
import logging
import random
import re
from typing import Any, Dict, List, Optional, Tuple

from clients.upstream import (
    DharmicDataClient,
    HavyakaApiClient,
    RigVedaApiClient,
    UpanishadSourceClient,
)
from constants.api import JAVA_MAX_INT
from constants.hindu import VEDA_STANZA_SPLIT_PATTERN, YAJUR_SPLIT_PATTERN
from constants.scriptures import (
    UPANISHAD_ALIASES,
    UPANISHAD_DEVOTIONAL_FILES,
    UPANISHAD_JSON_FILES,
)
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import compact, ensure_found, suggestion_for
from schemas.dtos import (
    MantraDto,
    RigVedaVerseDto,
    UpanishadDto,
    UpanishadVerseDto,
    VedaDto,
)
from services.static_registry import StaticContentRegistry

logger = logging.getLogger(__name__)

_STANZA_SPLIT = re.compile(VEDA_STANZA_SPLIT_PATTERN)
_YAJUR_SPLIT = re.compile(YAJUR_SPLIT_PATTERN)
_JS_VERSE_RE = re.compile(
    r"\{\s*devanagari:\s*'((?:\\'|[^'])*)'\s*,\s*iast:\s*'((?:\\'|[^'])*)'"
    r"\s*,\s*english:\s*'((?:\\'|[^'])*)'\s*,\s*hindi:\s*'((?:\\'|[^'])*)'\s*\}",
    re.S,
)
_CHAPTER_SPLIT_RE = re.compile(r"\{\s*number:\s*(\d+)\s*,\s*titleEnglish:")
_ABOUT_EN_RE = re.compile(r'about:\s*\{\s*en:\s*"((?:\\.|[^"\\])*)"', re.S)
_VERSE_MARK_RE = re.compile(r"॥\s*([0-9०-९]+)\s*॥")
_DEV_DIGIT_TRANS = str.maketrans("०१२३४५६७८९", "0123456789")


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _unescape_js(value: str) -> str:
    return (
        value.replace("\\'", "'")
        .replace('\\"', '"')
        .replace("\\n", "\n")
        .replace("\\\\", "\\")
        .strip()
    )


def _clean_sanskrit(text: str) -> str:
    return re.sub(r"\s*,\s*", " ", (text or "").replace("\xa0", " ")).strip()


def canonical_upanishad_id(value: str) -> str:
    key = compact(value).replace("upanishad", "").replace("upanishat", "")
    return UPANISHAD_ALIASES.get(key, key)


def _verse_number(sanskrit: str, fallback: int) -> int:
    marks = _VERSE_MARK_RE.findall((sanskrit or "").translate(_DEV_DIGIT_TRANS))
    if not marks:
        return fallback
    try:
        return int(marks[-1])
    except ValueError:
        return fallback


def _parse_devotional_verses(
        upanishad_id: str, script: str
) -> Tuple[Optional[str], List[UpanishadVerseDto]]:
    about = _ABOUT_EN_RE.search(script)
    description = _unescape_js(about.group(1)) if about else None
    verses: List[UpanishadVerseDto] = []
    chunks = _CHAPTER_SPLIT_RE.split(script)
    idx = 1
    while idx + 1 < len(chunks):
        chapter = _as_int(chunks[idx], 1)
        body = chunks[idx + 1]
        for i, (deva, iast, english, hindi) in enumerate(
                _JS_VERSE_RE.findall(body), start=1
        ):
            sanskrit = _unescape_js(deva)
            fallback = 0 if i == 1 else i
            verses.append(
                UpanishadVerseDto(
                    upanishadId=upanishad_id,
                    chapter=chapter,
                    verse=_verse_number(sanskrit, fallback),
                    sanskrit=sanskrit or None,
                    transliteration=_unescape_js(iast) or None,
                    translation=_unescape_js(english) or None,
                    hindiTranslation=_unescape_js(hindi) or None,
                )
            )
        idx += 2
    return description, verses


def _parse_json_verses(
        upanishad_id: str, raw: Dict[str, Any]
) -> List[UpanishadVerseDto]:
    mantras = raw.get("mantras")
    if not isinstance(mantras, list):
        return []
    prefix_to_chapter: Dict[Tuple[int, ...], int] = {}
    verses: List[UpanishadVerseDto] = []
    for item in mantras:
        if not isinstance(item, dict):
            continue
        number_raw = str(item.get("mantra_number") or "")
        sanskrit = _clean_sanskrit(str(item.get("sanskrit") or ""))
        if "इति" in number_raw or not sanskrit:
            continue
        nums = [_as_int(part) for part in re.findall(r"\d+", number_raw)]
        nums = [n for n in nums if n]
        if not nums:
            continue
        if len(nums) >= 3:
            prefix: Tuple[int, ...] = (nums[0], nums[1])
            verse = nums[-1]
        elif len(nums) == 2:
            prefix = (nums[0],)
            verse = nums[1]
        else:
            prefix = (1,)
            verse = nums[0]
        if prefix not in prefix_to_chapter:
            prefix_to_chapter[prefix] = len(prefix_to_chapter) + 1
        verses.append(
            UpanishadVerseDto(
                upanishadId=upanishad_id,
                chapter=prefix_to_chapter[prefix],
                verse=verse,
                sanskrit=sanskrit,
                transliteration=str(item.get("transliteration") or "") or None,
                translation=str(item.get("english") or item.get("translation") or "")
                            or None,
            )
        )
    return verses


def _split_stanzas(text: str) -> List[str]:
    parts = [p.strip() for p in _STANZA_SPLIT.split(text or "") if p.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _map_rig_verse(r: Dict[str, Any]) -> RigVedaVerseDto:
    return RigVedaVerseDto(
        mandala=_as_int(r.get("mandala", r.get("mandal"))),
        sukta=_as_int(r.get("sukta")),
        stanza=_as_int(r.get("stanza"), 1),
        text=r.get("text") or r.get("sanskrit"),
        poet=r.get("sungby") or r.get("poet"),
        poetCategory=r.get("sungbycategory") or r.get("poetCategory"),
        deity=r.get("sungfor") or r.get("deity"),
        deityCategory=r.get("sungforcategory") or r.get("deityCategory"),
        meter=r.get("meter"),
    )


def _map_dharmic_sukta(r: Dict[str, Any]) -> List[RigVedaVerseDto]:
    mandala = _as_int(r.get("mandala"))
    sukta = _as_int(r.get("sukta"))
    chunks = _split_stanzas(str(r.get("text") or ""))
    if not chunks:
        return []
    return [
        RigVedaVerseDto(mandala=mandala, sukta=sukta, stanza=i, text=chunk)
        for i, chunk in enumerate(chunks, start=1)
    ]


def _map_havyaka_mantra(raw: Dict[str, Any]) -> MantraDto:
    text = str(raw.get("shloka") or raw.get("text") or raw.get("devanagari") or "")
    return MantraDto(
        id=str(raw.get("_id") or raw.get("id") or ""),
        name=str(raw.get("name", "")) or None,
        text=text or None,
        devanagari=text or None,
        meaning=str(raw.get("purpose") or raw.get("meaning") or "") or None,
        deity=str(raw.get("godName") or raw.get("deity") or "") or None,
        tags=[],
    )


def _mantras_from_rows(rows: List[Dict[str, Any]], veda_name: str) -> List[MantraDto]:
    result: List[MantraDto] = []
    for i, m in enumerate(rows):
        if not isinstance(m, dict):
            continue
        text = str(m.get("text") or "")
        if veda_name.lower() == "yajur":
            chunks = [c.strip() for c in _YAJUR_SPLIT.split(text) if c.strip()]
            adhyaya = _as_int(m.get("adhyaya"), i + 1)
            if not chunks:
                chunks = [text] if text else []
            for idx, chunk in enumerate(chunks, start=1):
                result.append(
                    MantraDto(
                        id=f"yajur_{adhyaya}_{idx}",
                        name=f"Yajur Veda Adhyaya {adhyaya}.{idx}",
                        text=chunk,
                        veda="Yajur",
                    )
                )
            continue
        result.append(
            MantraDto(
                id=str(m.get("id") or f"{veda_name.lower()}_{i + 1}"),
                name=str(m.get("name") or m.get("deity") or "") or None,
                text=text or None,
                meaning=str(m.get("meaning") or "") or None,
                deity=str(m.get("deity") or "") or None,
                veda=veda_name,
            )
        )
    return result


class DefaultVedaService:
    def __init__(
            self,
            rig: RigVedaApiClient,
            havyaka: HavyakaApiClient,
            dharmic: DharmicDataClient,
            upanishads: UpanishadSourceClient,
            static: StaticContentRegistry,
    ) -> None:
        self._rig = rig
        self._havyaka = havyaka
        self._dharmic = dharmic
        self._upanishads = upanishads
        self._static = static

    async def get_all_vedas(self) -> List[VedaDto]:
        return [VedaDto.model_validate(x) for x in self._static.get_all_vedas()]

    async def get_veda(self, veda_id: str) -> VedaDto:
        for v in self._static.get_all_vedas():
            if str(v.get("vedaId", "")).lower() == veda_id.lower():
                return VedaDto.model_validate(v)
        names = [
            str(item.get("vedaId") or item.get("name") or "")
            for item in self._static.get_all_vedas()
        ]
        raise ResourceNotFoundError(
            "Veda", veda_id, suggestion=suggestion_for(veda_id, names)
        )

    async def get_rig_veda_by_mandala(
            self, mandala: int, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        dharmic = await self._dharmic.get_rig_veda_mandala(mandala)
        if dharmic:
            all_v = [verse for row in dharmic for verse in _map_dharmic_sukta(row)]
        else:
            api_list = await self._rig.get_by_mandala(mandala)
            if api_list:
                all_v = [_map_rig_verse(x) for x in api_list]
            else:
                all_v = [
                    RigVedaVerseDto.model_validate(x)
                    for x in self._static.get_rig_veda_verses(mandala)
                ]
        if not all_v:
            raise ResourceNotFoundError(
                "Rig Veda mandala",
                str(mandala),
                suggestion="Try searching: 1",
            )
        return paginate(all_v, page, size)

    async def get_rig_veda_by_deity(
            self, deity: str, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_deity(deity)
        if api_list:
            all_v = [_map_rig_verse(x) for x in api_list]
        else:
            needle = deity.strip().lower()
            all_v = [
                RigVedaVerseDto.model_validate(x)
                for x in self._static.get_rig_veda_verses(None)
                if str(x.get("deity", "")).lower() == needle
            ]
        if not all_v:
            names = [
                str(x.get("deity") or "")
                for x in self._static.get_rig_veda_verses(None)
            ]
            ensure_found(
                all_v, resource="Rig Veda deity", identifier=deity, available=names
            )
        return paginate(all_v, page, size)

    async def get_rig_veda_by_poet(
            self, poet: str, page: int, size: int
    ) -> List[RigVedaVerseDto]:
        api_list = await self._rig.get_by_poet(poet)
        if api_list:
            all_v = [_map_rig_verse(x) for x in api_list]
        else:
            needle = poet.strip().lower()
            all_v = [
                RigVedaVerseDto.model_validate(x)
                for x in self._static.get_rig_veda_verses(None)
                if str(x.get("poet", "")).lower() == needle
            ]
        if not all_v:
            names = [
                str(x.get("poet") or "") for x in self._static.get_rig_veda_verses(None)
            ]
            ensure_found(
                all_v, resource="Rig Veda poet", identifier=poet, available=names
            )
        return paginate(all_v, page, size)

    async def get_rig_veda_verse(
            self, mandala: int, sukta: int, stanza: int
    ) -> RigVedaVerseDto:
        all_v = await self.get_rig_veda_by_mandala(mandala, 0, JAVA_MAX_INT)
        for v in all_v:
            if v.sukta == sukta and v.stanza == stanza:
                return v
        raise ResourceNotFoundError("Rig Veda verse", f"{mandala}/{sukta}/{stanza}")

    async def get_yajur_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._dharmic.get_yajur_veda()
        if raw:
            all_m = _mantras_from_rows(raw, "Yajur")
        else:
            all_m = [
                MantraDto.model_validate(x)
                for x in self._static.get_veda_mantras("yajur")
            ]
        return paginate(all_m, page, size)

    async def get_sama_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        raw = await self._dharmic.get_sama_veda()
        if raw:
            all_m = _mantras_from_rows(raw, "Sama")
        else:
            havyaka = await self._havyaka.get_mantras_by_name("sama", 500)
            if havyaka:
                all_m = [_map_havyaka_mantra(x) for x in havyaka]
            else:
                all_m = [
                    MantraDto.model_validate(x)
                    for x in self._static.get_veda_mantras("sama")
                ]
        return paginate(all_m, page, size)

    async def get_atharva_veda_mantras(self, page: int, size: int) -> List[MantraDto]:
        sem = asyncio.Semaphore(4)

        async def load_kanda(kanda: int) -> List[Dict[str, Any]]:
            async with sem:
                rows = await self._dharmic.get_atharva_veda(kanda)
                return rows or []

        loaded = await asyncio.gather(*[load_kanda(k) for k in range(1, 6)])
        rows = [item for group in loaded for item in group]
        if rows:
            all_m = _mantras_from_rows(rows, "Atharva")
        else:
            all_m = [
                MantraDto.model_validate(x)
                for x in self._static.get_veda_mantras("atharva")
            ]
        return paginate(all_m, page, size)

    def _upanishad_names(self) -> List[str]:
        names: List[str] = []
        for item in self._static.get_all_upanishads():
            names.extend(
                [str(item.get("id") or ""), str(item.get("name") or "")]
            )
        return names

    def _upanishad_catalog(self, upanishad_id: str) -> Dict[str, Any]:
        wanted = canonical_upanishad_id(upanishad_id)
        for row in self._static.get_all_upanishads():
            if canonical_upanishad_id(str(row.get("id") or "")) == wanted:
                return dict(row)
        raise ResourceNotFoundError(
            "Upanishad",
            upanishad_id,
            suggestion=suggestion_for(upanishad_id, self._upanishad_names()),
        )

    async def _load_upanishad_verses(
            self, upanishad_id: str
    ) -> Tuple[Optional[str], List[UpanishadVerseDto]]:
        script_file = UPANISHAD_DEVOTIONAL_FILES.get(upanishad_id)
        if script_file:
            script = await self._upanishads.get_devotional_script(script_file)
            if script:
                description, verses = _parse_devotional_verses(upanishad_id, script)
                if verses:
                    return description, verses
        json_file = UPANISHAD_JSON_FILES.get(upanishad_id)
        if json_file:
            raw = await self._upanishads.get_sacred_json(json_file)
            if raw:
                verses = _parse_json_verses(upanishad_id, raw)
                if verses:
                    return None, verses
        static_rows = self._static.get_upanishad_verses(upanishad_id)
        return None, [UpanishadVerseDto.model_validate(x) for x in static_rows]

    def _upanishad_dto(
            self,
            row: Dict[str, Any],
            verses: List[UpanishadVerseDto],
            description: Optional[str] = None,
            *,
            include_verses: bool,
    ) -> UpanishadDto:
        dto = UpanishadDto.model_validate(row)
        if description:
            dto.description = description
        dto.verseCount = len(verses)
        chapters = {item.chapter for item in verses if item.chapter}
        if chapters:
            dto.chapters = max(chapters)
        if include_verses:
            dto.verses = verses
        return dto

    async def get_upanishads(self) -> List[UpanishadDto]:
        return [
            UpanishadDto.model_validate(x) for x in self._static.get_all_upanishads()
        ]

    async def get_upanishad(self, upanishad_id: str) -> UpanishadDto:
        row = self._upanishad_catalog(upanishad_id)
        canonical = str(row.get("id") or canonical_upanishad_id(upanishad_id))
        description, verses = await self._load_upanishad_verses(canonical)
        return self._upanishad_dto(
            row, verses, description, include_verses=True
        )

    async def get_upanishad_verses(
            self,
            upanishad_id: str,
            chapter: Optional[int],
            page: int,
            size: int,
    ) -> List[UpanishadVerseDto]:
        row = self._upanishad_catalog(upanishad_id)
        canonical = str(row.get("id") or canonical_upanishad_id(upanishad_id))
        _description, verses = await self._load_upanishad_verses(canonical)
        if chapter is not None:
            available = sorted({item.chapter for item in verses if item.chapter})
            verses = [item for item in verses if item.chapter == chapter]
            if not verses:
                suggestion = (
                    f"Try searching: {available[0]}" if available else "Try searching: 1"
                )
                raise ResourceNotFoundError(
                    "Upanishad chapter",
                    f"{upanishad_id}/{chapter}",
                    suggestion=suggestion,
                )
        elif not verses:
            raise ResourceNotFoundError(
                "Upanishad verses",
                upanishad_id,
                suggestion=suggestion_for(upanishad_id, self._upanishad_names()),
            )
        return paginate(verses, page, size)

    async def get_upanishad_verse(
            self, upanishad_id: str, chapter: int, verse: int
    ) -> UpanishadVerseDto:
        all_v = await self.get_upanishad_verses(
            upanishad_id, chapter, 0, JAVA_MAX_INT
        )
        for item in all_v:
            if item.verse == verse:
                return item
        raise ResourceNotFoundError(
            "Upanishad verse", f"{upanishad_id}/{chapter}/{verse}"
        )

    async def get_random_vedic_mantra(self) -> MantraDto:
        pool = self._static.get_veda_mantras(None)
        if not pool:
            return MantraDto(text="ॐ", meaning="The primordial sound")
        return MantraDto.model_validate(random.choice(pool))

    async def search_mantras(self, deity: str, limit: int) -> List[MantraDto]:
        raw = await self._havyaka.get_mantras_by_name(deity, limit)
        if raw:
            return [_map_havyaka_mantra(x) for x in raw][:limit]
        rows = self._static.get_mantras(deity, limit)
        mapped = [MantraDto.model_validate(x) for x in rows]
        if mapped:
            return mapped
        pool = self._static.get_mantras(None, 9999)
        names = [str(item.get("deity") or "") for item in pool] + [
            str(item.get("name") or "") for item in pool
        ]
        ensure_found(mapped, resource="Mantra", identifier=deity, available=names)
