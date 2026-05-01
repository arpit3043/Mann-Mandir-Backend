from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


async def get_json(
    client: httpx.AsyncClient,
    url: str,
    *,
    max_retries: int = 2,
    backoff_ms: float = 400.0,
) -> Optional[Any]:
    for attempt in range(max_retries):
        try:
            response = await client.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.warning("HTTP %s for %s: %s", e.response.status_code, url, e)
            return None
        except httpx.RequestError as e:
            logger.error("Request error for %s (attempt %s): %s", url, attempt + 1, e)
            if attempt >= max_retries - 1:
                return None
            await asyncio.sleep((backoff_ms / 1000.0) * (2**attempt))
    return None
