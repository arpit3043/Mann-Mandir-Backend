from typing import Optional

from fastapi import APIRouter, Depends, Request

from api.mantra_api.service_contract import MantraService
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


def get_mantra_service(request: Request) -> MantraService:
    return request.app.state.services.mantra


@router.get("")
async def list_mantras(
    deity: Optional[str] = None,
    page: int = 0,
    size: int = 20,
    svc: MantraService = Depends(get_mantra_service)
):
    full = await svc.get_mantras(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/random")
async def get_random_mantra(svc: MantraService = Depends(get_mantra_service)):
    return ok_payload(await svc.get_random_mantra())
