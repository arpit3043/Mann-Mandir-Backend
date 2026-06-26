from __future__ import annotations

import logging
import time as _time
import datetime
from typing import Optional, Dict, Any, Tuple

import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from api.responses import ok_payload
from core.config import Settings

logger = logging.getLogger(__name__)

router = APIRouter()


async def _proxy_json(
    *,
    request: Request,
    path: str,
    method: str = "GET",
    params: Optional[dict] = None,
    json_body: Optional[dict] = None,
):
    settings: Settings = request.app.state.settings
    base = settings.astro_api_base.rstrip("/") if settings.astro_api_base else ""
    key = settings.astro_api_key
    if not base or not key:
        raise HTTPException(status_code=400, detail="Astro API not configured on server")

    url = f"{base}/{path.lstrip('/')}"
    timeout = httpx.Timeout(
        settings.webclient_timeout_read,
        connect=settings.webclient_timeout_connect,
        write=settings.webclient_timeout_write,
    )
    async with httpx.AsyncClient(
        timeout=timeout,
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": key},
    ) as client:
        resp = await client.request(method, url, params=params, json=json_body)
        if resp.status_code < 200 or resp.status_code >= 300:
            logger.error("Astrology upstream error (%s): %s", path, resp.text.strip())
            return JSONResponse(
                status_code=502,
                content={"detail": "Upstream service unavailable"},
            )

        return ok_payload(resp.json())


@router.get("/horoscope/daily")
async def proxy_daily_horoscope(request: Request, sign: str):
    url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}&day=today"
    settings: Settings = request.app.state.settings
    timeout = httpx.Timeout(
        settings.webclient_timeout_read,
        connect=settings.webclient_timeout_connect,
        write=settings.webclient_timeout_write,
    )
    async with httpx.AsyncClient(timeout=timeout, headers={"Accept": "application/json"}, follow_redirects=True) as client:
        resp = await client.request("GET", url)
        if resp.status_code < 200 or resp.status_code >= 300:
            logger.error("Daily horoscope upstream error: %s", resp.text.strip())
            return JSONResponse(
                status_code=502,
                content={"detail": "Upstream service unavailable"},
            )

        resp_json = resp.json()
        data = resp_json.get("data", resp_json)
        return ok_payload(data)


# ---------------------------------------------------------------------------
# In-memory daily cache for Panchang
# ---------------------------------------------------------------------------
# The Free Astrology API enforces strict per-second rate limits. Panchang
# data is valid for an entire calendar day for a given location, so there is
# no reason to call the upstream API more than once per (date, location) pair.
#
# Structure: _panchang_cache[cache_key] = (payload_dict, expires_at_timestamp)
# ---------------------------------------------------------------------------
_panchang_cache: Dict[Tuple, Tuple[Dict[str, Any], float]] = {}


def _make_cache_key(year: int, month: int, date: int, lat: float, lon: float, tz: float) -> Tuple:
    """Round lat/lon to 2 decimal places so nearby locations share a cache entry."""
    return (year, month, date, round(lat, 2), round(lon, 2), tz)


def _cache_get(key: Tuple) -> Optional[Dict[str, Any]]:
    entry = _panchang_cache.get(key)
    if entry is None:
        return None
    payload, expires_at = entry
    if _time.time() > expires_at:
        del _panchang_cache[key]
        return None
    return payload


def _cache_set(key: Tuple, payload: Dict[str, Any], year: int, month: int, date: int) -> None:
    """Cache until midnight of the next day (max 24 h) so stale entries self-clean."""
    try:
        requested_date = datetime.date(year, month, date)
        next_day = requested_date + datetime.timedelta(days=1)
        expires_at = _time.mktime(next_day.timetuple())
    except (ValueError, OverflowError):
        expires_at = _time.time() + 86400  # fallback: 24 hours

    _panchang_cache[key] = (payload, expires_at)

    # Opportunistically evict expired entries to prevent unbounded memory growth
    now = _time.time()
    expired_keys = [k for k, (_, exp) in _panchang_cache.items() if exp < now]
    for k in expired_keys:
        _panchang_cache.pop(k, None)


@router.get("/panchang")
async def proxy_panchang(
    request: Request,
    year: int,
    month: int,
    date: int,
    lat: float,
    lon: float,
    tz: Optional[float] = None,
    hours: int = 6,
    minutes: int = 0,
    seconds: int = 0,
):
    import asyncio
    import json as _json

    resolved_tz = tz if tz is not None else 5.5

    # ------------------------------------------------------------------
    # Cache look-up — return immediately if we already have today's data
    # ------------------------------------------------------------------
    cache_key = _make_cache_key(year, month, date, lat, lon, resolved_tz)
    cached = _cache_get(cache_key)
    if cached is not None:
        logger.info("Panchang cache hit for key=%s", cache_key)
        return ok_payload(cached)

    settings: Settings = request.app.state.settings
    base = settings.astro_api_base.rstrip("/") if settings.astro_api_base else "https://json.freeastrologyapi.com"
    key = settings.astro_api_key
    if not key:
        return JSONResponse(status_code=400, content={"detail": "Astro API key not configured"})

    body = {
        'year': year,
        'month': month,
        'date': date,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'latitude': lat,
        'longitude': lon,
        'timezone': resolved_tz,
        'config': {
            'observation_point': 'topocentric',
            'ayanamsha': 'lahiri',
        },
    }

    timeout = httpx.Timeout(
        settings.webclient_timeout_read,
        connect=settings.webclient_timeout_connect,
        write=settings.webclient_timeout_write,
    )

    async def fetch_endpoint(client: httpx.AsyncClient, path: str):
        url = f"{base}/{path}"
        try:
            resp = await client.post(url, json=body)
            if resp.status_code == 200:
                out = resp.json().get("output")
                for _ in range(3):
                    if not isinstance(out, str):
                        break
                    try:
                        out = _json.loads(out)
                    except Exception:
                        break
                return out
            else:
                logger.warning("Upstream %s returned %s", path, resp.status_code)
        except Exception as exc:
            logger.warning("Error fetching %s: %s", path, exc)
        return None

    sem = asyncio.Semaphore(1)

    async def fetch_endpoint_throttled(client: httpx.AsyncClient, path: str):
        async with sem:
            await asyncio.sleep(0.5)  # 500 ms between requests to stay under rate limit
            return await fetch_endpoint(client, path)

    async with httpx.AsyncClient(
        timeout=timeout,
        headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": key},
    ) as client:
        tasks = [
            fetch_endpoint_throttled(client, "tithi-durations"),
            fetch_endpoint_throttled(client, "nakshatra-durations"),
            fetch_endpoint_throttled(client, "getsunriseandset"),
            fetch_endpoint_throttled(client, "yoga-durations"),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        tithi     = results[0] if not isinstance(results[0], Exception) else None
        nakshatra = results[1] if not isinstance(results[1], Exception) else None
        sun       = results[2] if not isinstance(results[2], Exception) else None
        yoga      = results[3] if not isinstance(results[3], Exception) else None

    if not tithi and not nakshatra and not sun:
        return JSONResponse(status_code=502, content={"detail": "Upstream rate limit or connection error"})

    output: Dict[str, Any] = {}
    if tithi:
        output["tithi"] = tithi
    if nakshatra:
        output["nakshatra"] = nakshatra
    if sun:
        assert isinstance(sun, dict), "sun must be a dict"
        output.update(sun)
    if yoga:
        output["yoga"] = yoga

    # ------------------------------------------------------------------
    # Store in cache — subsequent requests today skip all upstream calls
    # ------------------------------------------------------------------
    _cache_set(cache_key, output, year, month, date)
    logger.info("Panchang cached for key=%s", cache_key)

    return ok_payload(output)
