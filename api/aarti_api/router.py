from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import Request

from api.aarti_api.service_contract import AartiService
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


def get_aarti_service(request: Request) -> AartiService:
    return request.app.state.services.aarti


@router.get("")
async def list_aartis(
    deity: Optional[str] = None,
    page: int = 0,
    size: int = 20,
    svc: AartiService = Depends(get_aarti_service)
):
    full = await svc.get_aartis(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/deities")
async def list_aarti_deities(svc: AartiService = Depends(get_aarti_service)):
    return ok_payload(await svc.get_aarti_deities())


@router.get("/{aarti_id}")
async def get_aarti(aarti_id: str, svc: AartiService = Depends(get_aarti_service)):
    return ok_payload(await svc.get_aarti_by_id(aarti_id))
