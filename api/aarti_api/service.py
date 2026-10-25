from __future__ import annotations

from typing import List, Optional

from api.aarti_api.service_contract import AartiService
from core.exceptions import ResourceNotFoundError
from core.pagination import paginate
from core.suggestions import (
    catalog_labels,
    closest_row,
    ensure_found,
    norm,
    suggestion_from_row,
)
from schemas.dtos import AartiDto
from services.static_registry import StaticContentRegistry


class DefaultAartiService(AartiService):
    def __init__(self, static: StaticContentRegistry) -> None:
        self._static = static

    async def get_aartis(
        self, deity: Optional[str], page: int, size: int
    ) -> List[AartiDto]:
        rows = self._static.get_all_aartis()
        if deity and deity.strip():
            wanted = deity.strip().lower()
            matched = [
                row for row in rows if str(row.get("deity") or "").lower() == wanted
            ]
            ensure_found(
                matched,
                resource="Aarti",
                identifier=deity,
                available=catalog_labels(rows, "deity", "id"),
            )
            rows = matched
        return [AartiDto.model_validate(row) for row in paginate(rows, page, size)]

    async def get_aarti_by_id(self, aarti_id: str) -> AartiDto:
        wanted = norm(aarti_id)
        for row in self._static.get_all_aartis():
            if norm(str(row.get("id") or "")) == wanted:
                return AartiDto.model_validate(row)
        raise ResourceNotFoundError(
            "Aarti",
            aarti_id,
            suggestion=self._not_found_suggestion(aarti_id),
        )

    async def get_aarti_deities(self) -> List[str]:
        return sorted(
            {
                str(row["deity"])
                for row in self._static.get_all_aartis()
                if row.get("deity")
            }
        )

    def _not_found_suggestion(self, aarti_id: str) -> str:
        rows = self._static.get_all_aartis()
        return suggestion_from_row(
            closest_row(aarti_id, rows),
            fallback="Try searching /api/v1/god/aartis/deities for available names",
        )
