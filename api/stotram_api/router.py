from typing import Optional

from fastapi import APIRouter, Depends, Request

from api.stotram_api.service_contract import StotramService
from api.responses import ok_payload
from core.pagination import JAVA_MAX_INT, paginate as slice_page

router = APIRouter()


def get_stotram_service(request: Request) -> StotramService:
    return request.app.state.services.stotram


@router.get("")
async def list_stotrams(
    deity: Optional[str] = None,
    page: int = 0,
    size: int = 20,
    svc: StotramService = Depends(get_stotram_service)
):
    full = await svc.get_stotrams(deity, 0, JAVA_MAX_INT)
    data = slice_page(full, page, size)
    return ok_payload(data, page=page, size=size, total=len(full))


@router.get("/{stotram_id}")
async def get_stotram(stotram_id: str, svc: StotramService = Depends(get_stotram_service)):
    return ok_payload(await svc.get_stotram_by_id(stotram_id))
