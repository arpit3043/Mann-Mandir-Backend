from typing import Any, Dict, List, Optional

from api.scriptures_api.gita_api.service_contract import GitaService
from clients.upstream import DharmicDataClient, GitaTheAumClient, GitaVedicClient
from core.exceptions import ResourceNotFoundError
from schemas.dtos import GitaChapterDto, GitaVerseDto
from services.static_registry import StaticContentRegistry

_EN_TRANSLATION_KEYS = (
    "swami sivananda",
    "shri purohit swami",
    "swami gambirananda",
    "swami adidevananda",
    "dr. s. sankaranarayan",
)
_HI_TRANSLATION_KEYS = (
    "swami tejomayananda",
    "swami ramsukhdas",
    "sri harikrishnadas goenka",
)
_COMMENTARY_AUTHORS = (
    "Swami Sivananda",
    "Swami Gambirananda",
    "Sri Shankaracharya",
)


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _localized_text(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("en", "hi"):
            if value.get(key):
                return str(value[key])
        for val in value.values():
            if val:
                return str(val)
        return ""
    return str(value) if value else ""


def _map_theaum_chapter(
    c: Dict[str, Any], *, include_summary: bool = True
) -> GitaChapterDto:
    summary = _localized_text(c.get("summary")) if include_summary else None
    return GitaChapterDto(
        number=_as_int(c.get("chapter_number", c.get("number"))),
        name=str(c.get("name", "")),
        translation=str(
            c.get("translation") or _localized_text(c.get("meaning")) or ""
        ),
        transliteration=str(c.get("transliteration", "")),
        summary=summary or None,
        versesCount=_as_int(c.get("verses_count", c.get("versesCount"))),
    )


def _pick_translations(raw: Any) -> Dict[str, str]:
    translations: Dict[str, str] = {}
    if not isinstance(raw, dict):
        return translations
    lowered = {str(k).strip().lower(): str(val) for k, val in raw.items() if val}
    for key in _EN_TRANSLATION_KEYS:
        if lowered.get(key):
            translations["en"] = lowered[key]
            break
    for key in _HI_TRANSLATION_KEYS:
        if lowered.get(key):
            translations["hi"] = lowered[key]
            break
    return translations


def _pick_commentaries(raw: Any) -> Optional[Dict[str, str]]:
    if not isinstance(raw, dict):
        return None
    out: Dict[str, str] = {}
    for author in _COMMENTARY_AUTHORS:
        value = raw.get(author)
        if value:
            text = str(value).strip()
            out[author] = text[:2000]
    return out or None


def _map_dharmic_verse(
    chapter_number: int, v: Dict[str, Any], *, include_commentaries: bool = False
) -> GitaVerseDto:
    verse = _as_int(v.get("verse"))
    translations = _pick_translations(v.get("translations"))
    return GitaVerseDto(
        bgId=str(v.get("bgId") or v.get("_id") or f"BG{chapter_number}.{verse}"),
        chapter=_as_int(v.get("chapter"), chapter_number),
        verse=verse,
        shloka=str(v.get("text") or v.get("slok") or v.get("shloka") or "") or None,
        transliteration=str(v.get("transliteration") or "") or None,
        translations=translations or None,
        commentaries=_pick_commentaries(v.get("commentaries"))
        if include_commentaries
        else None,
    )


def _map_gita_verse(
    chapter_number: int, v: Dict[str, Any], verse_number: Optional[int] = None
) -> GitaVerseDto:
    verse = verse_number if verse_number is not None else _as_int(v.get("verse"))
    translations: Dict[str, str] = {}
    if isinstance(v.get("translations"), dict):
        translations = {str(k): str(val) for k, val in v["translations"].items() if val}
    siva = v.get("siva") if isinstance(v.get("siva"), dict) else {}
    tej = v.get("tej") if isinstance(v.get("tej"), dict) else {}
    if siva.get("et"):
        translations.setdefault("en", str(siva["et"]))
    if tej.get("ht"):
        translations.setdefault("hi", str(tej["ht"]))
    if v.get("wordMeanings"):
        translations.setdefault("en", str(v.get("wordMeanings")))
    if v.get("word_meanings"):
        translations.setdefault("en", str(v.get("word_meanings")))

    commentaries: Dict[str, str] = {}
    if isinstance(v.get("commentaries"), dict):
        commentaries = {str(k): str(val) for k, val in v["commentaries"].items() if val}

    return GitaVerseDto(
        bgId=str(v.get("bgId") or v.get("_id") or f"BG{chapter_number}.{verse}"),
        chapter=_as_int(v.get("chapter"), chapter_number),
        verse=verse,
        shloka=str(v.get("slok") or v.get("shloka") or v.get("text") or "") or None,
        transliteration=str(v.get("transliteration") or "") or None,
        translations=translations or None,
        commentaries=commentaries or None,
    )


class DefaultGitaService(GitaService):
    def __init__(
        self,
        gita_theaum: GitaTheAumClient,
        gita_vedic: GitaVedicClient,
        dharmic: DharmicDataClient,
        static: StaticContentRegistry,
    ) -> None:
        self._gita_theaum = gita_theaum
        self._gita_vedic = gita_vedic
        self._dharmic = dharmic
        self._static = static

    def _static_chapters(self, *, include_summary: bool) -> List[GitaChapterDto]:
        return [
            _map_theaum_chapter(x, include_summary=include_summary)
            for x in self._static.get_gita_chapters()
        ]

    async def get_gita_chapters(self) -> List[GitaChapterDto]:
        raw = await self._gita_theaum.get_all_chapters()
        if raw:
            return [
                _map_theaum_chapter(x, include_summary=False)
                for x in raw
                if isinstance(x, dict)
            ]
        return self._static_chapters(include_summary=False)

    async def get_gita_chapter(self, chapter_number: int) -> GitaChapterDto:
        raw = await self._gita_theaum.get_chapter(chapter_number)
        if isinstance(raw, dict) and not isinstance(raw, list):
            mapped = _map_theaum_chapter(raw, include_summary=True)
            if mapped.number:
                return mapped
        for mapped in self._static_chapters(include_summary=True):
            if mapped.number == chapter_number:
                return mapped
        raise ResourceNotFoundError(
            "Gita chapter",
            str(chapter_number),
            suggestion="Try searching: 1",
        )

    async def _dharmic_verses(
        self, chapter_number: int, *, include_commentaries: bool
    ) -> List[GitaVerseDto]:
        raw = await self._dharmic.get_gita_chapter_verses(chapter_number)
        if not raw:
            return []
        return [
            _map_dharmic_verse(
                chapter_number, v, include_commentaries=include_commentaries
            )
            for v in raw
            if isinstance(v, dict)
        ]

    async def get_gita_verses_by_chapter(
        self, chapter_number: int
    ) -> List[GitaVerseDto]:
        verses = await self._dharmic_verses(chapter_number, include_commentaries=False)
        if verses:
            return verses

        static_verses = self._static.get_gita_verses(chapter_number)
        mapped = [GitaVerseDto.model_validate(x) for x in static_verses]
        if mapped:
            return mapped
        raise ResourceNotFoundError(
            "Gita verses",
            str(chapter_number),
            suggestion="Try searching: 1",
        )

    async def get_gita_verse(
        self, chapter_number: int, verse_number: int
    ) -> GitaVerseDto:
        verses = await self._dharmic_verses(chapter_number, include_commentaries=True)
        for verse in verses:
            if verse.verse == verse_number:
                return verse

        v = await self._gita_vedic.get_slok(chapter_number, verse_number)
        if v:
            return _map_gita_verse(chapter_number, v, verse_number=verse_number)

        for vr in self._static.get_gita_verses(chapter_number):
            if _as_int(vr.get("verse")) == verse_number:
                return GitaVerseDto.model_validate(vr)
        raise ResourceNotFoundError(
            "Gita verse",
            f"{chapter_number}.{verse_number}",
            suggestion="Try searching: 1.1",
        )
