from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from clients.http_utils import get_json
from core.config import Settings


class GitaTheAumClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_gita_theaum_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_verse(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/text/{chapter}/{verse}"))

    async def get_chapter_verses(self, chapter: int) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url(f"/text/{chapter}"))
        return data if isinstance(data, list) else None

    async def get_chapter(self, chapter: int) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/chapter/{chapter}"))

    async def get_all_chapters(self) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url("/chapters/"))
        return data if isinstance(data, list) else None

    async def get_verse_translations(
        self, chapter: int, verse: int
    ) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/text/translations/{chapter}/{verse}"))

    async def get_verse_commentary(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/text/commentaries/{chapter}/{verse}"))


class GitaVedicClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_gita_vedic_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_slok(self, chapter: int, verse: int) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/slok/{chapter}/{verse}"))

    async def get_all_chapters(self) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url("/chapters"))
        return data if isinstance(data, list) else None


class DharmicDataClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_dharmicdata_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_mahabharata_parva(self, parva_number: int) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/mahabharata/parva-{parva_number}.json"))

    async def get_ramayana_kanda(self, kanda: str) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url(f"/ramayana/{kanda}.json"))

    async def get_yajur_veda(self) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url("/yajurveda/yajurveda.json"))

    async def get_atharva_veda(self) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url("/atharvaveda/atharvaveda.json"))


class HanumanChalisaClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_chalisa_hanuman_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_all_verses(self) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url("/hanumanChalisa.json"))
        return data if isinstance(data, list) else None


class HavyakaApiClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_havyaka_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_mantras(self, limit: int) -> Optional[List[Dict[str, Any]]]:
        wrapped = await get_json(self._http, self._url(f"/mantras?limit={limit}"))
        return self._unwrap(wrapped)

    async def get_mantras_by_name(self, name: str, limit: int) -> Optional[List[Dict[str, Any]]]:
        wrapped = await get_json(self._http, self._url(f"/mantras?name={name}&limit={limit}"))
        return self._unwrap(wrapped)

    def _unwrap(self, wrapped: Optional[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        if not wrapped or not isinstance(wrapped, dict):
            return None
        raw = wrapped.get("mantras")
        if not isinstance(raw, list):
            return None
        out: List[Dict[str, Any]] = []
        for item in raw:
            if isinstance(item, dict):
                out.append(item)
        return out


class ShlokaApiClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_shloka_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_random_shloka(self) -> Optional[Dict[str, Any]]:
        return await get_json(self._http, self._url("/sanskrit/slogan/random"))


class RigVedaApiClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._settings = settings

    def _url(self, path: str) -> str:
        base = self._settings.api_rigveda_base_url.rstrip("/")
        return base + (path if path.startswith("/") else "/" + path)

    async def get_by_mandala(self, mandala: int) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url(f"/meta/book/{mandala}"))
        return data if isinstance(data, list) else None

    async def get_by_deity(self, deity: str) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url(f"/meta/god/{deity}"))
        return data if isinstance(data, list) else None

    async def get_by_poet(self, poet: str) -> Optional[List[Dict[str, Any]]]:
        data = await get_json(self._http, self._url(f"/meta/poet/{poet}"))
        return data if isinstance(data, list) else None
