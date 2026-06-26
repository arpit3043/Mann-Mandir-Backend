from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import httpx
import pybreaker

from clients.http_utils import get_json_cached
from core.config import Settings

if TYPE_CHECKING:
    from core.cache import RedisCache

logger = logging.getLogger(__name__)

_gita_theaum_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_gita_vedic_breaker  = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_dharmic_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_hanuman_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_havyaka_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_shloka_breaker      = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_rig_veda_breaker    = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])


class GitaTheAumClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_default_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_gita_theaum_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_gita_theaum_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — GitaTheAum unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("GitaTheAum request failed: %s", exc)
            return None

    async def get_verse(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/text/{chapter}/{verse}")

    async def get_chapter_verses(self, chapter: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/text/{chapter}")
        return data if isinstance(data, list) else None

    async def get_chapter(self, chapter: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/chapter/{chapter}")

    async def get_all_chapters(self) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get("/chapters/")
        return data if isinstance(data, list) else None

    async def get_verse_translations(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/text/translations/{chapter}/{verse}")

    async def get_verse_commentary(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/text/commentaries/{chapter}/{verse}")


class GitaVedicClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_default_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_gita_vedic_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_gita_vedic_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — GitaVedic unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("GitaVedic request failed: %s", exc)
            return None

    async def get_slok(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/slok/{chapter}/{verse}")

    async def get_all_chapters(self) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get("/chapters")
        return data if isinstance(data, list) else None

    async def get_verses_for_chapter(self, chapter: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/sloks/{chapter}")
        return data if isinstance(data, list) else None


class DharmicDataClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_default_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_dharmicdata_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_dharmic_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — DharmicData unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("DharmicData request failed: %s", exc)
            return None

    async def get_mahabharata_parva(self, parva_number: int) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/mahabharata/parva-{parva_number}.json")

    async def get_ramayana_kanda(self, kanda: str) -> Optional[Dict[str, Any]]:
        return await self._safe_get(f"/ramayana/{kanda}.json")

    async def get_yajur_veda(self) -> Optional[Dict[str, Any]]:
        return await self._safe_get("/yajurveda/yajurveda.json")

    async def get_atharva_veda(self) -> Optional[Dict[str, Any]]:
        return await self._safe_get("/atharvaveda/atharvaveda.json")


class HanumanChalisaClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_default_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_chalisa_hanuman_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_hanuman_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — HanumanChalisa unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("HanumanChalisa request failed: %s", exc)
            return None

    async def get_all_verses(self) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get("/hanumanChalisa.json")
        return data if isinstance(data, list) else None


class HavyakaApiClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_medium_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_havyaka_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_havyaka_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — Havyaka unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("Havyaka request failed: %s", exc)
            return None

    async def get_mantras(self, limit: int) -> Optional[List[Dict[str, Any]]]:
        return self._unwrap(await self._safe_get(f"/mantras?limit={limit}"))

    async def get_mantras_by_name(self, name: str, limit: int) -> Optional[List[Dict[str, Any]]]:
        return self._unwrap(await self._safe_get(f"/mantras?name={name}&limit={limit}"))

    def _unwrap(self, wrapped: Optional[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        if not wrapped or not isinstance(wrapped, dict):
            return None
        raw = wrapped.get("mantras")
        if not isinstance(raw, list):
            return None
        return [item for item in raw if isinstance(item, dict)]


class ShlokaApiClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_short_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_shloka_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_shloka_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — Shloka API unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("Shloka request failed: %s", exc)
            return None

    async def get_random_shloka(self) -> Optional[Dict[str, Any]]:
        return await self._safe_get("/sanskrit/slogan/random")


class RigVedaApiClient:
    def __init__(
        self,
        http: httpx.AsyncClient,
        settings: Settings,
        cache: Optional[RedisCache] = None,
    ) -> None:
        self._http = http
        self._settings = settings
        self._cache = cache
        self._ttl = settings.redis_default_ttl

    def _url(self, path: str) -> str:
        base = self._settings.api_rigveda_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    @_rig_veda_breaker
    async def _get(self, path: str) -> Optional[Any]:
        return await get_json_cached(self._http, self._url(path), self._cache, self._ttl)

    async def _safe_get(self, path: str) -> Optional[Any]:
        try:
            return await self._get(path)
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — RigVeda API unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("RigVeda request failed: %s", exc)
            return None

    async def get_by_mandala(self, mandala: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/meta/book/{mandala}")
        return data if isinstance(data, list) else None

    async def get_by_deity(self, deity: str) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/meta/god/{deity}")
        return data if isinstance(data, list) else None

    async def get_by_poet(self, poet: str) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/meta/poet/{poet}")
        return data if isinstance(data, list) else None
