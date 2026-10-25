from __future__ import annotations

from typing import Any, Dict, List, Optional

from api.stotram_api.service_contract import StotramService
from clients.upstream import DrikPanchangStotramClient
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import closest_row, deity_key, norm, suggestion_from_row
from schemas.dtos import StotramDto, StotramVerseDto
from services.static_registry import StaticContentRegistry


class DefaultStotramService(StotramService):
    def __init__(
        self,
        static: StaticContentRegistry,
        drik: Optional[DrikPanchangStotramClient] = None,
    ) -> None:
        self.static = static
        self.drik = drik

    async def _catalog(self) -> List[Dict[str, Any]]:
        rows = [dict(item) for item in self.static.get_all_stotrams()]
        seen = {str(item.get("id") or "").lower() for item in rows}
        if not self.drik:
            return rows
        remote = await self.drik.get_collection()
        path_by_id = {str(item.get("id") or "").lower(): item.get("path") for item in remote}
        for row in rows:
            cid = str(row.get("id") or "").lower()
            if cid in path_by_id:
                row["path"] = path_by_id[cid]
        for item in remote:
            cid = str(item.get("id") or "").lower()
            if not cid or cid in seen:
                continue
            seen.add(cid)
            rows.append(
                {
                    "id": item["id"],
                    "name": item.get("name") or item["id"],
                    "deity": item.get("deity") or item.get("name") or item["id"],
                    "author": None,
                    "description": None,
                    "verseCount": 0,
                    "verses": [],
                    "path": item.get("path"),
                }
            )
        return rows

    def _find_row(self, stotram_id: str, rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        wanted = norm(stotram_id)
        prefixed = wanted if wanted.startswith("stotram-") else f"stotram-{wanted}"
        for row in rows:
            sid = norm(str(row.get("id") or ""))
            name = norm(str(row.get("name") or ""))
            aliases = {sid, sid.removeprefix("stotram-"), name}
            if wanted in aliases or prefixed in aliases:
                return row
        return None

    def _not_found_suggestion(self, query: str, rows: List[Dict[str, Any]]) -> str:
        return suggestion_from_row(
            closest_row(query, rows),
            fallback="Try searching /api/v1/god/stotram/deities for available names",
        )

    async def get_stotram_deities(self) -> List[str]:
        rows = await self._catalog()
        return sorted({str(row["deity"]) for row in rows if row.get("deity")})

    async def get_stotrams(self, deity: Optional[str], page: int, size: int) -> List[StotramDto]:
        rows = await self._catalog()
        if deity and deity.strip():
            wanted = deity_key(deity)
            matched = [row for row in rows if deity_key(str(row.get("deity") or "")) == wanted]
            if not matched:
                raise ResourceNotFoundError(
                    "Stotram",
                    deity,
                    suggestion=self._not_found_suggestion(deity, rows),
                )
            rows = matched
        items = [StotramDto.model_validate(row) for row in paginate(rows, page, size)]
        for item in items:
            item.verses = None
        return items

    async def get_stotram_by_id(self, stotram_id: str) -> StotramDto:
        rows = await self._catalog()
        row = self._find_row(stotram_id, rows)
        if not row:
            raise ResourceNotFoundError(
                "Stotram",
                stotram_id,
                suggestion=self._not_found_suggestion(stotram_id, rows),
            )
        dto = StotramDto.model_validate(row)
        verses = [verse for verse in (dto.verses or []) if verse.sanskrit or verse.transliteration or verse.meaning]
        if verses:
            dto.verses = verses
            dto.verseCount = len(verses)
            return dto
        if self.drik:
            remote = await self.drik.get_verses(str(row.get("id") or stotram_id), path=row.get("path"))
            if remote:
                dto.verses = [StotramVerseDto.model_validate(item) for item in remote]
                dto.verseCount = len(dto.verses)
                return dto
        dto.verses = verses or None
        return dto
