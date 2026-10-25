from typing import Optional

from fastapi import APIRouter, Depends, Request

from api.mantra_api.service_contract import MantraService
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT
from core.pagination import paginate as slice_page

router = APIRouter()


def get_mantra_service(request: Request) -> MantraService:
    return request.app.state.services.mantra


@router.get("/random")
async def get_random_mantra(
    date: Optional[str] = None,
    svc: MantraService = Depends(get_mantra_service),
):
    return ok_payload(await svc.get_random_mantra(date))


@router.get("")
async def list_mantras(
    deity: Optional[str] = None,
    page: int = 0,
    size: int = 20,
    limit: Optional[int] = None,
    svc: MantraService = Depends(get_mantra_service),
):
    page_size = limit if limit is not None else size
    full = await svc.get_mantras(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, page_size)
    return ok_payload(data, page=page, size=page_size, total=len(full))
