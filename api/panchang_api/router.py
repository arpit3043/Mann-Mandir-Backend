from fastapi import APIRouter, Depends, Request

from api.panchang_api.service_contract import PanchangService
from api.responses import ok_payload

router = APIRouter()


def get_panchang_service(request: Request) -> PanchangService:
    return request.app.state.services.panchang


@router.get("/today")
async def panchang_today(svc: PanchangService = Depends(get_panchang_service)):
    return ok_payload(await svc.get_panchang_today())


@router.get("/date/{date}")
async def panchang_by_date(date: str, svc: PanchangService = Depends(get_panchang_service)):
    return ok_payload(await svc.get_panchang_by_date(date))


@router.get("/horoscope/daily/{sign}")
async def daily_horoscope(sign: str, svc: PanchangService = Depends(get_panchang_service)):
    return ok_payload(await svc.get_daily_horoscope(sign))
