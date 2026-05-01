from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi.encoders import jsonable_encoder

from schemas.api_response import meta_from_totals


def ok_payload(
    data: Any,
    *,
    page: Optional[int] = None,
    size: Optional[int] = None,
    total: Optional[int] = None,
) -> dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    body: dict[str, Any] = {"success": True, "data": jsonable_encoder(data), "timestamp": ts}
    if page is not None and size is not None and total is not None:
        meta = meta_from_totals(page, size, total)
        body["paginationMeta"] = meta.model_dump(by_alias=True)
    return body
