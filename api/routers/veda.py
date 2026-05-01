from fastapi import APIRouter

from api.deps import VedaSvc
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


@router.get("")
async def list_vedas(svc: VedaSvc):
    return ok_payload(await svc.get_all_vedas())


@router.get("/rig/mandalas/{mandala}/verses")
async def rig_by_mandala(mandala: int, svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_rig_veda_by_mandala(mandala, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/rig/mandalas/{mandala}/suktas/{sukta}/stanzas/{stanza}")
async def rig_verse(mandala: int, sukta: int, stanza: int, svc: VedaSvc):
    return ok_payload(await svc.get_rig_veda_verse(mandala, sukta, stanza))


@router.get("/rig/search/deity/{deity}")
async def rig_by_deity(deity: str, svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_rig_veda_by_deity(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/rig/search/poet/{poet}")
async def rig_by_poet(poet: str, svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_rig_veda_by_poet(poet, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/yajur/mantras")
async def yajur_mantras(svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_yajur_veda_mantras(0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/sama/mantras")
async def sama_mantras(svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_sama_veda_mantras(0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/atharva/mantras")
async def atharva_mantras(svc: VedaSvc, page: int = 0, size: int = 20):
    full = await svc.get_atharva_veda_mantras(0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/mantras/random")
async def random_vedic_mantra(svc: VedaSvc):
    return ok_payload(await svc.get_random_vedic_mantra())


@router.get("/mantras/search")
async def search_mantras(svc: VedaSvc, deity: str, limit: int = 20):
    return ok_payload(await svc.search_mantras(deity, limit))


@router.get("/upanishads")
async def list_upanishads(svc: VedaSvc):
    return ok_payload(await svc.get_upanishads())


@router.get("/upanishads/{upanishad_id}")
async def get_upanishad(upanishad_id: str, svc: VedaSvc):
    return ok_payload(await svc.get_upanishad(upanishad_id))


@router.get("/upanishads/{upanishad_id}/chapters/{chapter}/verses")
async def upanishad_verses(
    upanishad_id: str, chapter: int, svc: VedaSvc, page: int = 0, size: int = 20
):
    full = await svc.get_upanishad_verses(upanishad_id, chapter, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/upanishads/{upanishad_id}/chapters/{chapter}/verses/{verse}")
async def upanishad_verse(upanishad_id: str, chapter: int, verse: int, svc: VedaSvc):
    return ok_payload(await svc.get_upanishad_verse(upanishad_id, chapter, verse))


@router.get("/{veda_id}")
async def get_veda(veda_id: str, svc: VedaSvc):
    return ok_payload(await svc.get_veda(veda_id))
