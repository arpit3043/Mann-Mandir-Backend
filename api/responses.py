from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

from fastapi.encoders import jsonable_encoder

from core.exceptions import ResourceNotFoundError
from core.request_context import identifier_from_request
from core.suggestions import suggestion_for
from schemas.api_response import ApiResponse, meta_from_totals


def ok_payload(
        data: Any,
        *,
        page: Optional[int] = None,
        size: Optional[int] = None,
        total: Optional[int] = None,
        resource: Optional[str] = None,
        query: Optional[str] = None,
        available: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    encoded = jsonable_encoder(data)
    empty_list = isinstance(encoded, list) and len(encoded) == 0
    empty_collection = empty_list and (total is None or total == 0)
    if empty_collection:
        inferred_resource, inferred_query = identifier_from_request()
        label = resource or inferred_resource
        ident = (query or inferred_query or "requested data").strip()
        choices: Sequence[str] = [str(item) for item in (available or []) if item]
        raise ResourceNotFoundError(
            label,
            ident,
            suggestion=suggestion_for(
                ident,
                choices,
                fallback="Try a different spelling or browse without filters",
            ),
        )
    pagination = None
    if page is not None and size is not None and total is not None:
        pagination = meta_from_totals(page, size, total)
    return ApiResponse.ok_data(encoded, pagination).model_dump(
        mode="json", exclude_none=True
    )
