from typing import Optional

from fastapi import APIRouter

from api.deps import GodSvc
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


@router.get("/aartis")
async def list_aartis(
    svc: GodSvc,
    deity: Optional[str] = None,
    page: int = 0,
    size: int = 20,
):
    full = await svc.get_aartis(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/aartis/deities")
async def list_aarti_deities(svc: GodSvc):
    return ok_payload(await svc.get_aarti_deities())


@router.get("/aartis/{aarti_id}")
async def get_aarti(aarti_id: str, svc: GodSvc):
    return ok_payload(await svc.get_aarti_by_id(aarti_id))


@router.get("/chalisas")
async def list_chalisas(svc: GodSvc, page: int = 0, size: int = 20):
    full = await svc.get_chalisas(0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/chalisas/{deity}/verses/{verse_number}")
async def get_chalisa_verse(deity: str, verse_number: int, svc: GodSvc):
    return ok_payload(await svc.get_chalisa_verse(deity, verse_number))


@router.get("/chalisas/{deity}")
async def get_chalisa(deity: str, svc: GodSvc):
    return ok_payload(await svc.get_chalisa_by_deity(deity))


@router.get("/stotram")
async def list_stotrams(svc: GodSvc, deity: Optional[str] = None, page: int = 0, size: int = 20):
    full = await svc.get_stotrams(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/stotram/{stotram_id}")
async def get_stotram(stotram_id: str, svc: GodSvc):
    return ok_payload(await svc.get_stotram_by_id(stotram_id))


@router.get("/mantras/random")
async def random_mantra(svc: GodSvc):
    return ok_payload(await svc.get_random_mantra())


@router.get("/mantras")
async def list_mantras(svc: GodSvc, deity: Optional[str] = None, limit: int = 20):
    return ok_payload(await svc.get_mantras(deity, limit))
