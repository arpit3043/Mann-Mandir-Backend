from typing import Any, Dict, List, Optional

from api.chalisa_api.service_contract import ChalisaService
from clients.upstream import DrikPanchangChalisaClient, HanumanChalisaClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import catalog_labels, ensure_found, suggestion_for
from schemas.dtos import ChalisaDto, ChalisaVerseDto
from services.static_registry import StaticContentRegistry


def _english_from_translations(raw: Any) -> Optional[str]:
    if isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                continue
            text = item.get("translation")
            if text:
                return str(text)
    if isinstance(raw, dict):
        return str(raw.get("en") or raw.get("english") or "") or None
    return None


def _map_verse(raw: Dict[str, Any]) -> ChalisaVerseDto:
    verse_no = raw.get("verseNumber", raw.get("id", raw.get("verse_number", 0)))
    try:
        verse_number = int(verse_no)
    except (TypeError, ValueError):
        verse_number = 0
    return ChalisaVerseDto(
        verseNumber=verse_number,
        type=str(raw.get("meter") or raw.get("type") or "") or None,
        devanagari=raw.get("verse") or raw.get("devanagari"),
        transliteration=raw.get("transliteration"),
        englishTranslation=_english_from_translations(raw.get("translations"))
                           or raw.get("englishTranslation"),
        hindiTranslation=raw.get("hindiTranslation"),
        tags=raw.get("tags") if isinstance(raw.get("tags"), list) else None,
    )


class DefaultChalisaService(ChalisaService):
    def __init__(
            self,
            hanuman: HanumanChalisaClient,
            drik: DrikPanchangChalisaClient,
            static: StaticContentRegistry,
    ) -> None:
        self.hanuman = hanuman
        self.drik = drik
        self.static = static

    def _static_row(self, chalisa_id: str) -> Optional[Dict[str, Any]]:
        wanted = chalisa_id.strip().lower()
        prefixed = wanted if wanted.startswith("chalisa-") else f"chalisa-{wanted}"
        for c in self.static.get_all_chalisas():
            cid = str(c.get("id", "")).lower()
            deity = str(c.get("deity", "")).lower()
            if cid == wanted or cid == prefixed or deity == wanted:
                return c
        return None

    async def _catalog(self) -> List[Dict[str, Any]]:
        rows = [dict(c) for c in self.static.get_all_chalisas()]
        seen = {str(c.get("id", "")).lower() for c in rows}
        remote = await self.drik.get_collection()
        for item in remote:
            cid = str(item.get("id") or "").lower()
            if not cid or cid in seen:
                continue
            seen.add(cid)
            rows.append(
                {
                    "id": item["id"],
                    "deity": item.get("deity") or item.get("title") or item["id"],
                    "title": item.get("title") or item["id"],
                    "totalVerses": 40,
                    "path": item.get("path"),
                }
            )
        return rows

    async def _find_chalisa(self, chalisa_id: str) -> Optional[Dict[str, Any]]:
        found = self._static_row(chalisa_id)
        if found:
            path = self.drik.path_for_id(str(found.get("id") or ""))
            if path:
                found = dict(found)
                found["path"] = path
            return found
        wanted = chalisa_id.strip().lower()
        prefixed = wanted if wanted.startswith("chalisa-") else f"chalisa-{wanted}"
        for item in await self.drik.get_collection():
            cid = str(item.get("id") or "").lower()
            deity = str(item.get("deity") or "").lower()
            title = str(item.get("title") or "").lower()
            if (
                    cid in {wanted, prefixed}
                    or deity == wanted
                    or prefixed in title.replace(" ", "-")
            ):
                return {
                    "id": item["id"],
                    "deity": item.get("deity") or item.get("title") or item["id"],
                    "title": item.get("title") or item["id"],
                    "totalVerses": 40,
                    "path": item.get("path"),
                }
        return None

    async def _verses_for(self, chalisa: Dict[str, Any]) -> List[ChalisaVerseDto]:
        chalisa_id = str(chalisa.get("id", ""))
        if chalisa_id == "chalisa-hanuman":
            verses = await self.hanuman.get_all_verses()
            if verses:
                return [_map_verse(v) for v in verses if isinstance(v, dict)]

        remote = await self.drik.get_verses(chalisa_id, path=chalisa.get("path"))
        if remote:
            return [_map_verse(v) for v in remote]

        rows = self.static.get_chalisa_verses(chalisa_id)
        return [ChalisaVerseDto.model_validate(v) for v in rows]

    async def get_chalisas(
            self, deity: Optional[str], page: int, size: int
    ) -> List[ChalisaDto]:
        all_rows = await self._catalog()
        if deity and deity.strip():
            d = deity.strip().lower()
            matched = [c for c in all_rows if str(c.get("deity", "")).lower() == d]
            if not matched:
                ensure_found(
                    matched,
                    resource="Chalisa",
                    identifier=deity,
                    available=catalog_labels(all_rows, "deity", "id"),
                )
            all_rows = matched
        page_rows = paginate(all_rows, page, size)
        return [ChalisaDto.model_validate(x) for x in page_rows]

    async def get_chalisa_by_id(self, chalisa_id: str) -> ChalisaDto:
        found = await self._find_chalisa(chalisa_id)
        if not found:
            rows = await self._catalog()
            names = [str(c.get("id") or "") for c in rows] + [
                str(c.get("deity") or "") for c in rows
            ]
            raise ResourceNotFoundError(
                "Chalisa",
                chalisa_id,
                suggestion=suggestion_for(chalisa_id, names),
            )
        dto = ChalisaDto.model_validate(found)
        verses = await self._verses_for(found)
        if verses:
            dto.verses = verses
            dto.totalVerses = len(verses)
        return dto

    async def get_chalisa_verse(
            self, chalisa_id: str, verse_number: int
    ) -> ChalisaVerseDto:
        found = await self._find_chalisa(chalisa_id)
        if not found:
            rows = await self._catalog()
            names = [str(c.get("id") or "") for c in rows]
            raise ResourceNotFoundError(
                "Chalisa", chalisa_id, suggestion=suggestion_for(chalisa_id, names)
            )
        for verse in await self._verses_for(found):
            if verse.verseNumber == verse_number:
                return verse
        raise ResourceNotFoundError(
            "Chalisa verse",
            f"{chalisa_id}/{verse_number}",
            suggestion="Try searching: 1",
        )
