from typing import Optional

from fastapi import APIRouter

from api.deps import SearchSvc
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


@router.get("")
async def search(svc: SearchSvc, query: str, domain: Optional[str] = None, page: int = 0, size: int = 20):
    full = await svc.search(query, domain, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    total = await svc.count(query, domain)
    return ok_payload(data, page=page, size=size, total=total)
