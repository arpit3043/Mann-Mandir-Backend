from abc import ABC, abstractmethod
from typing import Any


class PanchangService(ABC):
    @abstractmethod
    async def get_panchang_today(self) -> Any:
        pass

    @abstractmethod
    async def get_panchang_by_date(self, date: str) -> Any:
        pass

    @abstractmethod
    async def get_daily_horoscope(self, sign: str) -> Any:
        pass
