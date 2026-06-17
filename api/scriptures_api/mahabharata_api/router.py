from fastapi import APIRouter, Depends, Request

from api.scriptures_api.mahabharata_api.service_contract import MahabharataService
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


def get_mahabharata_service(request: Request) -> MahabharataService:
    return request.app.state.services.mahabharata


@router.get("/parvas")
async def mahabharata_parvas(svc: MahabharataService = Depends(get_mahabharata_service)):
    return ok_payload(await svc.get_mahabharata_parvas())


@router.get("/parvas/{parva_number}")
async def mahabharata_parva(parva_number: int, svc: MahabharataService = Depends(get_mahabharata_service)):
    return ok_payload(await svc.get_mahabharata_parva(parva_number))


@router.get("/parvas/{parva_number}/chapters/{chapter_number}/verses")
async def mahabharata_verses(
    parva_number: int, chapter_number: int, svc: MahabharataService = Depends(get_mahabharata_service), page: int = 0, size: int = 20
):
    full = await svc.get_mahabharata_verses(parva_number, chapter_number, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/parvas/{parva_number}/chapters/{chapter_number}/verses/{verse}")
async def mahabharata_verse(parva_number: int, chapter_number: int, verse: int, svc: MahabharataService = Depends(get_mahabharata_service)):
    return ok_payload(await svc.get_mahabharata_verse(parva_number, chapter_number, verse))
