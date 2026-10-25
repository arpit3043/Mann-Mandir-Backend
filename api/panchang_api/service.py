from __future__ import annotations

import datetime as dt
import logging
import math
from typing import Any, Optional
from zoneinfo import ZoneInfo

import httpx

from api.panchang_api.service_contract import PanchangService
from constants.astrology import HOROSCOPE_DAILY_URL, ZODIAC_SIGNS
from constants.hindu import (
    AYANA_DAKSHINAYANA,
    AYANA_UTTARAYANA,
    IST_TIMEZONE,
    KRISHNA_AMAVASYA,
    NAKSHATRAS,
    PAKSHA_KRISHNA,
    PAKSHA_SHUKLA,
    RITU_BY_MONTH,
    TITHI_NAMES,
    UTTARAYANA_END_MONTH,
    UTTARAYANA_START_MONTH,
    WEEKDAYS,
    WEEKDAYS_HI,
    YOGA_NAMES,
)
from core.exceptions import ResourceNotFoundError
from core.suggestions import suggestion_for

logger = logging.getLogger(__name__)


def _julian_day(moment: dt.datetime) -> float:
    y = moment.year
    m = moment.month
    d = (
            moment.day
            + (moment.hour + moment.minute / 60.0 + moment.second / 3600.0) / 24.0
    )
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


def _sun_longitude(jd: float) -> float:
    n = jd - 2451545.0
    l = (280.460 + 0.9856474 * n) % 360
    g = math.radians((357.528 + 0.9856003 * n) % 360)
    return (l + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360


def _moon_longitude(jd: float) -> float:
    n = jd - 2451545.0
    l = (218.316 + 13.176396 * n) % 360
    m = math.radians((134.963 + 13.064993 * n) % 360)
    return (l + 6.289 * math.sin(m)) % 360


def _panchang_for(moment: dt.datetime) -> dict[str, Any]:
    jd = _julian_day(moment)
    sun = _sun_longitude(jd)
    moon = _moon_longitude(jd)
    elongation = (moon - sun) % 360
    tithi_index = int(elongation / 12)
    if tithi_index >= 15:
        paksha = PAKSHA_KRISHNA
        tithi_name = (
            KRISHNA_AMAVASYA if tithi_index == 29 else TITHI_NAMES[tithi_index - 15]
        )
        tithi_number = tithi_index - 14
    else:
        paksha = PAKSHA_SHUKLA
        tithi_name = TITHI_NAMES[tithi_index]
        tithi_number = tithi_index + 1
    nakshatra = NAKSHATRAS[int(moon / (360 / 27)) % 27]
    yoga = YOGA_NAMES[int(((moon + sun) % 360) / (360 / 27)) % 27]
    weekday = moment.weekday()
    month = moment.month
    ritu = RITU_BY_MONTH[month]
    ayana = (
        AYANA_UTTARAYANA
        if UTTARAYANA_START_MONTH <= month < UTTARAYANA_END_MONTH
        else AYANA_DAKSHINAYANA
    )
    return {
        "date": moment.date().isoformat(),
        "weekday": WEEKDAYS[weekday],
        "weekdayHindi": WEEKDAYS_HI[weekday],
        "tithi": tithi_name,
        "tithiNumber": tithi_number,
        "paksha": paksha,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "ritu": ritu,
        "ayana": ayana,
        "sunriseNote": "Local sunrise/sunset requires location; this calendar uses a geocentric lunar approximation.",
    }


class DefaultPanchangService(PanchangService):
    def __init__(self, http: Optional[httpx.AsyncClient] = None) -> None:
        self._http = http

    async def get_panchang_today(self) -> Any:
        return _panchang_for(dt.datetime.now(dt.timezone.utc).astimezone())

    async def get_panchang_by_date(self, date: str) -> Any:
        try:
            parsed = dt.date.fromisoformat(date.strip())
        except ValueError as exc:
            raise ValueError("date must be YYYY-MM-DD") from exc
        noon = dt.datetime.combine(
            parsed,
            dt.time(12, 0),
            tzinfo=ZoneInfo(IST_TIMEZONE),
        )
        return _panchang_for(noon)

    async def get_daily_horoscope(self, sign: str) -> Any:
        cleaned = (sign or "").strip().lower()
        if not cleaned:
            raise ValueError("sign is required")
        if cleaned not in ZODIAC_SIGNS:
            raise ResourceNotFoundError(
                "Horoscope sign",
                sign,
                suggestion=suggestion_for(cleaned, ZODIAC_SIGNS),
            )
        if self._http is None:
            return _panchang_for(dt.datetime.now(dt.timezone.utc).astimezone())
        url = f"{HOROSCOPE_DAILY_URL}?sign={cleaned}&day=today"
        try:
            resp = await self._http.get(url)
            if resp.status_code == 200:
                payload = resp.json()
                data = (
                    payload.get("data", payload)
                    if isinstance(payload, dict)
                    else payload
                )
                return {"sign": cleaned, "day": "today", "horoscope": data}
        except Exception as exc:
            logger.warning("Daily horoscope upstream failed: %s", exc)
        panchang = _panchang_for(dt.datetime.now(dt.timezone.utc).astimezone())
        return {
            "sign": cleaned,
            "day": "today",
            "panchang": panchang,
            "horoscope": None,
        }
