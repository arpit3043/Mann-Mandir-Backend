from fastapi import APIRouter, Depends, Request

from api.responses import ok_payload
from api.scriptures_api.ramayana_api.service_contract import RamayanaService
from constants.api import DEFAULT_PAGE_SIZE, JAVA_MAX_INT
from core.pagination import paginate as slice_page

router = APIRouter()


def get_ramayana_service(request: Request) -> RamayanaService:
    return request.app.state.services.ramayana


@router.get("/kandas")
async def ramayana_kandas(svc: RamayanaService = Depends(get_ramayana_service)):
    return ok_payload(await svc.get_ramayana_kandas())


@router.get("/kandas/{kanda_id}")
async def ramayana_kanda(
        kanda_id: str, svc: RamayanaService = Depends(get_ramayana_service)
):
    return ok_payload(await svc.get_ramayana_kanda(kanda_id))


@router.get("/kandas/{kanda_id}/sargas/{sarga}/verses")
async def ramayana_verses(
        kanda_id: str,
        sarga: int,
        svc: RamayanaService = Depends(get_ramayana_service),
        page: int = 0,
        size: int = DEFAULT_PAGE_SIZE,
):
    full = await svc.get_ramayana_verses(kanda_id, sarga, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/kandas/{kanda_id}/sargas/{sarga}/verses/{verse}")
async def ramayana_verse(
        kanda_id: str,
        sarga: int,
        verse: int,
        svc: RamayanaService = Depends(get_ramayana_service),
):
    return ok_payload(await svc.get_ramayana_verse(kanda_id, sarga, verse))
