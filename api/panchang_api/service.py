from __future__ import annotations

import datetime as dt
import logging
import math
from typing import Any, Optional

import httpx

from api.panchang_api.service_contract import PanchangService
from core.exceptions import ResourceNotFoundError
from core.suggestions import suggestion_for
from core.zodiac import ZODIAC_SIGNS

logger = logging.getLogger(__name__)

_TITHI_NAMES = [
    "Pratipada",
    "Dwitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dwadashi",
    "Trayodashi",
    "Chaturdashi",
    "Purnima",
]
_KRISHNA_15 = "Amavasya"
_NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
_YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti",
]
_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_WEEKDAYS_HI = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
_HOROSCOPE_URL = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"


def _julian_day(moment: dt.datetime) -> float:
    y = moment.year
    m = moment.month
    d = moment.day + (moment.hour + moment.minute / 60.0 + moment.second / 3600.0) / 24.0
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
        paksha = "Krishna"
        tithi_name = _KRISHNA_15 if tithi_index == 29 else _TITHI_NAMES[tithi_index - 15]
        tithi_number = tithi_index - 14
    else:
        paksha = "Shukla"
        tithi_name = _TITHI_NAMES[tithi_index]
        tithi_number = tithi_index + 1
    nakshatra = _NAKSHATRAS[int(moon / (360 / 27)) % 27]
    yoga = _YOGA_NAMES[int(((moon + sun) % 360) / (360 / 27)) % 27]
    weekday = moment.weekday()
    month = moment.month
    if month in (4, 5):
        ritu = "Vasanta"
    elif month in (6, 7):
        ritu = "Grishma"
    elif month in (8, 9):
        ritu = "Varsha"
    elif month in (10, 11):
        ritu = "Sharad"
    elif month == 12 or month == 1:
        ritu = "Hemanta"
    else:
        ritu = "Shishira"
    ayana = "Uttarayana" if 3 <= month < 9 else "Dakshinayana"
    return {
        "date": moment.date().isoformat(),
        "weekday": _WEEKDAYS[weekday],
        "weekdayHindi": _WEEKDAYS_HI[weekday],
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
        noon = dt.datetime.combine(parsed, dt.time(12, 0), tzinfo=dt.timezone(dt.timedelta(hours=5, minutes=30)))
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
        url = f"{_HOROSCOPE_URL}?sign={cleaned}&day=today"
        try:
            resp = await self._http.get(url)
            if resp.status_code == 200:
                payload = resp.json()
                data = payload.get("data", payload) if isinstance(payload, dict) else payload
                return {"sign": cleaned, "day": "today", "horoscope": data}
        except Exception as exc:
            logger.warning("Daily horoscope upstream failed: %s", exc)
        panchang = _panchang_for(dt.datetime.now(dt.timezone.utc).astimezone())
        return {"sign": cleaned, "day": "today", "panchang": panchang, "horoscope": None}
