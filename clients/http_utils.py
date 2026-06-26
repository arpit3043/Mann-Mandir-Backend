from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

import httpx

if TYPE_CHECKING:
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
    return response.json()


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
