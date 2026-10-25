from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

from core.cache import RedisCache

logger = logging.getLogger(__name__)


async def get_json(
    client: httpx.AsyncClient,
    url: str,
) -> Optional[Any]:
    response = await client.get(url)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        logger.warning("Non-JSON response from %s (status=%s)", url, response.status_code)
        return None


async def get_json_cached(
    client: httpx.AsyncClient,
    url: str,
    cache: Optional[RedisCache],
    ttl: int,
) -> Optional[Any]:
    if cache is not None:
        key = cache.make_key(url)
        cached = cache.get(key)
        if cached is not None:
            logger.debug("Cache HIT  key=%r", key)
            return cached

    result = await get_json(client, url)

    if result is not None and cache is not None:
        key = cache.make_key(url)
        cache.set(key, result, ttl)
        logger.debug("Cache SET  key=%r  ttl=%ds", key, ttl)

    return result


_HTML_HEADERS = {
    "Accept": "text/html,application/xhtml+xml",
    "User-Agent": "Mozilla/5.0 (compatible; MannMandir/1.0)",
}


async def get_text(
    client: httpx.AsyncClient,
    url: str,
) -> Optional[str]:
    response = await client.get(url, headers=_HTML_HEADERS)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.text


async def get_text_cached(
    client: httpx.AsyncClient,
    url: str,
    cache: Optional[RedisCache],
    ttl: int,
) -> Optional[str]:
    if cache is not None:
        key = cache.make_key(url)
        cached = cache.get(key)
        if isinstance(cached, str):
            logger.debug("Cache HIT  key=%r", key)
            return cached

    result = await get_text(client, url)

    if result is not None and cache is not None:
        key = cache.make_key(url)
        cache.set(key, result, ttl)
        logger.debug("Cache SET  key=%r  ttl=%ds", key, ttl)

    return result
