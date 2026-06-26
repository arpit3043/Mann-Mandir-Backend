from typing import Any

from api.panchang_api.service_contract import PanchangService


class DefaultPanchangService(PanchangService):
    def __init__(self) -> None:
        pass

    async def get_panchang_today(self) -> Any:
        return {"message": "Panchang for today not yet implemented."}

    async def get_panchang_by_date(self, date: str) -> Any:
        return {"message": f"Panchang for {date} not yet implemented."}

    async def get_daily_horoscope(self, sign: str) -> Any:
        return {"message": f"Daily horoscope for {sign} not yet implemented."}
