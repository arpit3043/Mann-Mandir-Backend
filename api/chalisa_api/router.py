from typing import Optional

from fastapi import APIRouter, Depends, Request

from api.chalisa_api.service_contract import ChalisaService
from api.responses import ok_payload
from constants.api import DEFAULT_PAGE_SIZE, JAVA_MAX_INT
from core.pagination import paginate as slice_page

router = APIRouter()


def get_chalisa_service(request: Request) -> ChalisaService:
    return request.app.state.services.chalisa


@router.get("")
async def list_chalisas(
        deity: Optional[str] = None,
        page: int = 0,
        size: int = DEFAULT_PAGE_SIZE,
        svc: ChalisaService = Depends(get_chalisa_service),
):
    full = await svc.get_chalisas(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/{chalisa_id}/verses/{verse_number}")
async def get_chalisa_verse(
        chalisa_id: str,
        verse_number: int,
        svc: ChalisaService = Depends(get_chalisa_service),
):
    return ok_payload(await svc.get_chalisa_verse(chalisa_id, verse_number))


@router.get("/{chalisa_id}")
async def get_chalisa(
        chalisa_id: str, svc: ChalisaService = Depends(get_chalisa_service)
):
    return ok_payload(await svc.get_chalisa_by_id(chalisa_id))
