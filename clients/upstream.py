from __future__ import annotations

import logging
import re
from html import unescape
from typing import Any, Dict, List, Optional

import httpx
import pybreaker

from clients.http_utils import get_json_cached, get_text_cached
from core.cache import RedisCache
from core.config import Settings

logger = logging.getLogger(__name__)

_gita_theaum_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_gita_vedic_breaker  = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_dharmic_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_hanuman_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_havyaka_breaker     = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_shloka_breaker      = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_rig_veda_breaker    = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])
_drik_breaker        = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60, exclude=[httpx.HTTPStatusError])


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
        data = await self._safe_get(f"/chapter/{chapter}/")
        return data if isinstance(data, dict) else None

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
        data = await self._safe_get(f"/slok/{chapter}/{verse}/")
        return data if isinstance(data, dict) else None

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

    RAMAYANA_KANDA_FILES = {
        "bala": "1_balakanda.json",
        "balakanda": "1_balakanda.json",
        "ayodhya": "2_ayodhyakanda.json",
        "ayodhyakanda": "2_ayodhyakanda.json",
        "aranya": "3_aranyakanda.json",
        "aranyakanda": "3_aranyakanda.json",
        "kishkindha": "4_kishkindhakanda.json",
        "kishkindhakanda": "4_kishkindhakanda.json",
        "sundara": "5_sundarakanda.json",
        "sundarakanda": "5_sundarakanda.json",
        "yuddha": "6_yudhhakanda.json",
        "yudhha": "6_yudhhakanda.json",
        "yudhhakanda": "6_yudhhakanda.json",
        "lanka": "6_yudhhakanda.json",
        "uttara": "7_uttarakanda.json",
        "uttarakanda": "7_uttarakanda.json",
    }

    @staticmethod
    def _as_list(data: Optional[Any], *keys: str) -> Optional[List[Dict[str, Any]]]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            for key in keys:
                raw = data.get(key)
                if isinstance(raw, list):
                    return [item for item in raw if isinstance(item, dict)]
        return None

    async def get_gita_chapter_verses(self, chapter: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/SrimadBhagvadGita/bhagavad_gita_chapter_{chapter}.json")
        return self._as_list(data, "BhagavadGitaChapter")

    async def get_mahabharata_parva(self, parva_number: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/Mahabharata/mahabharata_book_{parva_number}.json")
        return self._as_list(data)

    async def get_ramayana_kanda(self, kanda: str) -> Optional[List[Dict[str, Any]]]:
        filename = self.RAMAYANA_KANDA_FILES.get(kanda.strip().lower())
        if not filename:
            return None
        data = await self._safe_get(f"/ValmikiRamayana/{filename}")
        return self._as_list(data)

    async def get_yajur_veda(self) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get("/Yajurveda/vajasneyi_madhyadina_samhita.json")
        return self._as_list(data)

    async def get_atharva_veda(self, kanda: int = 1) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/AtharvaVeda/atharvaveda_kaanda_{kanda}.json")
        return self._as_list(data)

    async def get_rig_veda_mandala(self, mandala: int) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get(f"/Rigveda/rigveda_mandala_{mandala}.json")
        return self._as_list(data)

    async def get_sama_veda(self) -> Optional[List[Dict[str, Any]]]:
        data = await self._safe_get("/Samaveda/Samaveda.json")
        return self._as_list(data, "verses")


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

    @staticmethod
    def _as_hymn_list(data: Optional[Any]) -> Optional[List[Dict[str, Any]]]:
        if isinstance(data, dict):
            hymns = data.get("hymns") or data.get("results")
            if isinstance(hymns, list):
                return [item for item in hymns if isinstance(item, dict)]
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        return None

    async def get_by_mandala(self, mandala: int) -> Optional[List[Dict[str, Any]]]:
        hymns = self._as_hymn_list(await self._safe_get(f"/hymns?mandal={mandala}"))
        if hymns:
            return hymns
        data = await self._safe_get(f"/meta/book/{mandala}")
        return data if isinstance(data, list) else None

    async def get_by_deity(self, deity: str) -> Optional[List[Dict[str, Any]]]:
        hymns = self._as_hymn_list(await self._safe_get(f"/hymns?sungfor={deity}"))
        if hymns:
            return hymns
        expanded = self._as_hymn_list(
            await self._safe_get(f"/sungfor/{deity}/mandals?expand=true")
        )
        if expanded:
            return expanded
        data = await self._safe_get(f"/meta/god/{deity}")
        return data if isinstance(data, list) else None

    async def get_by_poet(self, poet: str) -> Optional[List[Dict[str, Any]]]:
        hymns = self._as_hymn_list(await self._safe_get(f"/hymns?sungby={poet}"))
        if hymns:
            return hymns
        data = await self._safe_get(f"/meta/poet/{poet}")
        return data if isinstance(data, list) else None


class DrikPanchangClient:
    """Shared HTTP access for drikpanchang.com lyric pages."""

    COLLECTION_PATH = ""
    KNOWN_PATHS: Dict[str, str] = {}

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

    def _url(self, path: str, lang: str = "hi") -> str:
        base = self._settings.api_drikpanchang_base_url.rstrip("/")
        clean = path.split("?")[0]
        if not clean.startswith("/"):
            clean = "/" + clean
        return f"{base}{clean}?lang={lang}&ck=1"

    @_drik_breaker
    async def _get_html(self, url: str) -> Optional[str]:
        return await get_text_cached(self._http, url, self._cache, self._ttl)

    async def _safe_html(self, path: str, lang: str = "hi") -> Optional[str]:
        try:
            return await self._get_html(self._url(path, lang))
        except pybreaker.CircuitBreakerError:
            logger.warning("Circuit OPEN — DrikPanchang unavailable")
            return None
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error("DrikPanchang request failed: %s", exc)
            return None

    @staticmethod
    def _strip_tags(raw: str) -> str:
        text = re.sub(r"<[^>]+>", "", raw)
        return unescape(text).replace("\xa0", " ").strip()

    def path_for_id(self, item_id: str) -> Optional[str]:
        return self.KNOWN_PATHS.get(item_id.strip().lower())


class DrikPanchangChalisaClient(DrikPanchangClient):
    """Lyrics from drikpanchang.com chalisa collection pages."""

    COLLECTION_PATH = "/lyrics/chalisa/chalisa-collection.html"
    KNOWN_PATHS = {
        "chalisa-hanuman": "/lyrics/chalisa/lord-hanuman/shree-hanuman-chalisa.html",
        "chalisa-ganesh": "/lyrics/chalisa/lord-ganesha/shree-ganesha-chalisa.html",
        "chalisa-shiva": "/lyrics/chalisa/lord-shiva/shiva-chalisa.html",
        "chalisa-durga": "/lyrics/chalisa/durga-mata/durga-mata-chalisa.html",
        "chalisa-lakshmi": "/lyrics/chalisa/lakshmi-mata/lakshmi-mata-chalisa.html",
        "chalisa-saraswati": "/lyrics/chalisa/saraswati-mata/saraswati-mata-chalisa.html",
        "chalisa-ram": "/lyrics/chalisa/lord-rama/shree-rama-chalisa.html",
    }

    @staticmethod
    def _id_from_path(path: str) -> str:
        name = path.split("/")[-1].split("?")[0].replace(".html", "")
        name = re.sub(r"^(shree|shri|sri)-", "", name)
        name = re.sub(r"-chalisa$", "", name)
        return f"chalisa-{name}" if name else "chalisa-unknown"

    async def get_collection(self) -> List[Dict[str, str]]:
        html = await self._safe_html(self.COLLECTION_PATH, lang="en")
        if not html:
            return []
        path_to_id = {path: cid for cid, path in self.KNOWN_PATHS.items()}
        seen: set[str] = set()
        items: List[Dict[str, str]] = []
        card_re = re.compile(
            r'alt="([^"]+)"[\s\S]{0,400}?class="dpFestivalTitle">([^<]+)</div>\s*'
            r'<a href="(/lyrics/chalisa/[^"]+\.html)\?lang=en[^"]*"[\s\S]{0,300}?'
            r'href="(/lyrics/chalisa/[^"]+\.html)\?lang=hi',
            re.I,
        )
        for alt, title, _en_path, hi_path in card_re.findall(html):
            path = hi_path
            cid = path_to_id.get(path) or self._id_from_path(path)
            if cid in seen:
                continue
            seen.add(cid)
            deity = alt.replace("Lord ", "").replace(" Mata", "").strip()
            items.append(
                {
                    "id": cid,
                    "deity": deity or title.strip(),
                    "title": title.strip(),
                    "path": path,
                }
            )
        return items

    def _parse_verses(self, html: str) -> List[Dict[str, Any]]:
        current = "Chaupai"
        raw_verses: List[Dict[str, str]] = []
        token_re = re.compile(
            r'<h3 class="dpLyricsType[^"]*">([\s\S]*?)</h3>|<div class="dpLyricsChalisaGroup">([\s\S]*?)</div>'
        )
        for match in token_re.finditer(html):
            if match.group(1) is not None:
                heading = self._strip_tags(match.group(1))
                if "दोहा" in heading or "doha" in heading.lower():
                    current = "Doha"
                elif "चौपाई" in heading or "chaupai" in heading.lower():
                    current = "Chaupai"
                elif heading:
                    current = heading
                continue
            group = match.group(2) or ""
            for paragraph in re.findall(r'<p class="dpGroup">([\s\S]*?)</p>', group):
                rows = [
                    self._strip_tags(span)
                    for span in re.findall(r'<span class="dpRow">([\s\S]*?)</span>', paragraph)
                ]
                text = " ".join(row for row in rows if row).strip()
                if text:
                    raw_verses.append({"type": current, "devanagari": text})
        return self._merge_incomplete(raw_verses)

    @staticmethod
    def _merge_incomplete(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        merged: List[Dict[str, Any]] = []
        pending: Optional[Dict[str, str]] = None
        for row in rows:
            text = row["devanagari"]
            if pending is None:
                pending = dict(row)
            else:
                pending["devanagari"] = pending["devanagari"] + " " + text
            if "॥" in pending["devanagari"] or "||" in pending["devanagari"]:
                merged.append(pending)
                pending = None
        if pending:
            merged.append(pending)
        out: List[Dict[str, Any]] = []
        for i, item in enumerate(merged, start=1):
            verse_type = item.get("type") or "Chaupai"
            out.append(
                {
                    "verseNumber": i,
                    "type": verse_type,
                    "devanagari": item["devanagari"],
                    "transliteration": None,
                    "englishTranslation": None,
                    "tags": [verse_type],
                }
            )
        return out

    async def get_verses(self, chalisa_id: str, path: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        page = path or self.path_for_id(chalisa_id)
        if not page:
            collection = await self.get_collection()
            for item in collection:
                if item.get("id") == chalisa_id:
                    page = item.get("path")
                    break
        if not page:
            return None
        html = await self._safe_html(page, lang="hi")
        if not html:
            return None
        verses = self._parse_verses(html)
        return verses or None


class DrikPanchangStotramClient(DrikPanchangClient):
    """Lyrics from drikpanchang.com stotram collection pages."""

    COLLECTION_PATH = "/lyrics/stotram/stotram-collection.html"
    KNOWN_PATHS = {
        "stotram-shiva-tandava": "/lyrics/stotram/lord-shiva/shiva-tandav-stotram.html",
        "stotram-mahishasura-mardini": "/lyrics/stotram/durga/mahishasura-mardini/mahishasura-mardini-stotram.html",
        "stotram-aditya-hridayam": "/lyrics/stotram/lord-surya/aditya-hridaya-stotram.html",
        "stotram-ganesh-atharvashirsha": "/lyrics/stotram/lord-ganesha/ganapati-atharvashirsha-stotram.html",
    }

    @staticmethod
    def _id_from_path(path: str) -> str:
        name = path.split("/")[-1].split("?")[0].replace(".html", "")
        name = re.sub(r"^(shree|shri|sri)-", "", name)
        name = re.sub(r"-stotram$", "", name)
        return f"stotram-{name}" if name else "stotram-unknown"

    @staticmethod
    def _clean_deity(raw: str) -> str:
        deity = raw.replace("Goddess ", "").replace("Lord ", "").replace(" Mata", "").replace(" Deva", "").strip()
        return deity or raw.strip()

    async def get_collection(self) -> List[Dict[str, str]]:
        html = await self._safe_html(self.COLLECTION_PATH, lang="en")
        if not html:
            return []
        path_to_id = {path: cid for cid, path in self.KNOWN_PATHS.items()}
        seen: set[str] = set()
        items: List[Dict[str, str]] = []
        card_re = re.compile(
            r'alt="([^"]+)"[\s\S]{0,400}?class="dpFestivalTitle">([^<]+)</div>\s*'
            r'<a href="(/lyrics/stotram/[^"]+\.html)\?lang=en[^"]*"[\s\S]{0,300}?'
            r'href="(/lyrics/stotram/[^"]+\.html)\?lang=hi',
            re.I,
        )
        for alt, title, _en_path, hi_path in card_re.findall(html):
            path = hi_path
            cid = path_to_id.get(path) or self._id_from_path(path)
            if cid in seen:
                continue
            seen.add(cid)
            items.append(
                {
                    "id": cid,
                    "deity": self._clean_deity(alt) or title.strip(),
                    "name": title.strip(),
                    "path": path,
                }
            )
        return items

    def _parse_verses(self, html: str) -> List[Dict[str, Any]]:
        verses: List[Dict[str, Any]] = []
        for group in re.findall(r'<div class="dpLyricsAartiGroup">([\s\S]*?)</div>', html):
            lines: List[str] = []
            for paragraph in re.findall(r"<p>([\s\S]*?)</p>", group):
                rows = [
                    self._strip_tags(span)
                    for span in re.findall(r'<span class="dpRow">([\s\S]*?)</span>', paragraph)
                ]
                text = " ".join(row for row in rows if row).strip()
                if text:
                    lines.append(text)
            if not lines:
                continue
            verses.append(
                {
                    "verseNumber": len(verses) + 1,
                    "sanskrit": " ".join(lines),
                    "transliteration": None,
                    "meaning": None,
                }
            )
        return verses

    async def get_verses(self, stotram_id: str, path: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        page = path or self.path_for_id(stotram_id)
        if not page:
            collection = await self.get_collection()
            wanted = stotram_id.strip().lower()
            for item in collection:
                if str(item.get("id") or "").lower() == wanted:
                    page = item.get("path")
                    break
        if not page:
            return None
        html = await self._safe_html(page, lang="hi")
        if not html:
            return None
        verses = self._parse_verses(html)
        return verses or None

