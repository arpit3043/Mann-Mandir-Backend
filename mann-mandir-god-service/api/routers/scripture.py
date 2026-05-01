from fastapi import APIRouter

from api.deps import ScriptureSvc
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


@router.get("/gita/chapters")
async def gita_chapters(svc: ScriptureSvc):
    return ok_payload(await svc.get_gita_chapters())


@router.get("/gita/chapters/{chapter_number}")
async def gita_chapter(chapter_number: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_gita_chapter(chapter_number))


@router.get("/gita/chapters/{chapter_number}/verses")
async def gita_chapter_verses(chapter_number: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_gita_verses_by_chapter(chapter_number))


@router.get("/gita/chapters/{chapter_number}/verses/{verse_number}")
async def gita_verse(chapter_number: int, verse_number: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_gita_verse(chapter_number, verse_number))


@router.get("/ramayana/kandas")
async def ramayana_kandas(svc: ScriptureSvc):
    return ok_payload(await svc.get_ramayana_kandas())


@router.get("/ramayana/kandas/{kanda_id}")
async def ramayana_kanda(kanda_id: str, svc: ScriptureSvc):
    return ok_payload(await svc.get_ramayana_kanda(kanda_id))


@router.get("/ramayana/kandas/{kanda_id}/sargas/{sarga}/verses")
async def ramayana_verses(kanda_id: str, sarga: int, svc: ScriptureSvc, page: int = 0, size: int = 20):
    full = await svc.get_ramayana_verses(kanda_id, sarga, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/ramayana/kandas/{kanda_id}/sargas/{sarga}/verses/{verse}")
async def ramayana_verse(kanda_id: str, sarga: int, verse: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_ramayana_verse(kanda_id, sarga, verse))


@router.get("/mahabharata/parvas")
async def mahabharata_parvas(svc: ScriptureSvc):
    return ok_payload(await svc.get_mahabharata_parvas())


@router.get("/mahabharata/parvas/{parva_number}")
async def mahabharata_parva(parva_number: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_mahabharata_parva(parva_number))


@router.get("/mahabharata/parvas/{parva_number}/chapters/{chapter_number}/verses")
async def mahabharata_verses(
    parva_number: int, chapter_number: int, svc: ScriptureSvc, page: int = 0, size: int = 20
):
    full = await svc.get_mahabharata_verses(parva_number, chapter_number, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/mahabharata/parvas/{parva_number}/chapters/{chapter_number}/verses/{verse}")
async def mahabharata_verse(parva_number: int, chapter_number: int, verse: int, svc: ScriptureSvc):
    return ok_payload(await svc.get_mahabharata_verse(parva_number, chapter_number, verse))
