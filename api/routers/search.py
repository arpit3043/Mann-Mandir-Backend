from typing import Optional

from fastapi import APIRouter, Query

from api.deps import SearchSvc
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT
from core.pagination import paginate as slice_page

router = APIRouter()


@router.get("")
async def search(
    svc: SearchSvc,
    query: Optional[str] = Query(
        None,
        description="Generic full-text query. Example: shiva, laxmi, om namah shivaya",
    ),
    q: Optional[str] = Query(None, description="Alias for query"),
    type: Optional[str] = Query(
        None,
        description="Optional type filter: aarti, chalisa, stotram, mantra. Omit for generic search across all types.",
    ),
    domain: Optional[str] = Query(
        None,
        description="Optional domain: god, scriptures, vedas. Omit to search everything.",
    ),
    page: int = 0,
    size: int = 20,
):
    text = (query or q or "").strip()
    full = await svc.search(text, domain, 0, JAVA_MAX_INT, content_type=type)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))
