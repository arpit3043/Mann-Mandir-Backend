from fastapi import APIRouter, Depends, Request

from api.responses import ok_payload
from api.scriptures_api.gita_api.service_contract import GitaService

router = APIRouter()


def get_gita_service(request: Request) -> GitaService:
    return request.app.state.services.gita


@router.get("/chapters")
async def get_gita_chapters(svc: GitaService = Depends(get_gita_service)):
    return ok_payload(await svc.get_gita_chapters())


@router.get("/chapters/{chapter_number}")
async def get_gita_chapter(chapter_number: int, svc: GitaService = Depends(get_gita_service)):
    return ok_payload(await svc.get_gita_chapter(chapter_number))


@router.get("/chapters/{chapter_number}/verses")
async def get_gita_verses(chapter_number: int, svc: GitaService = Depends(get_gita_service)):
    return ok_payload(await svc.get_gita_verses_by_chapter(chapter_number))


@router.get("/chapters/{chapter_number}/verses/{verse_number}")
async def get_gita_verse(chapter_number: int, verse_number: int, svc: GitaService = Depends(get_gita_service)):
    return ok_payload(await svc.get_gita_verse(chapter_number, verse_number))
