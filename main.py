from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.deps import build_services

__version__ = "1.0.0"
from api.routers import veda
from api.routers import search
from api.routers import astro
from api.aarti_api import router as aarti_router
from api.chalisa_api import router as chalisa_router
from api.stotram_api import router as stotram_router
from api.mantra_api import router as mantra_router
from api.scriptures_api.gita_api import router as gita_router
from api.scriptures_api.ramayana_api import router as ramayana_router
from api.scriptures_api.mahabharata_api import router as mahabharata_router
from api.panchang_api import router as panchang_router
from core.cache import RedisCache, build_redis_cache
from core.config import Settings
from core.exceptions import ResourceNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_replica_specs(raw: str) -> list[tuple[str, int]]:
    """Parse 'host:port,host:port' into a list of (host, port) tuples."""
    specs: list[tuple[str, int]] = []
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        try:
            host, port_str = entry.rsplit(":", 1)
            specs.append((host.strip(), int(port_str.strip())))
        except ValueError:
            logger.warning("Invalid redis replica spec %r — skipping", entry)
    return specs


def _build_cache(s: Settings) -> Optional[RedisCache]:
    """
    Construct a RedisCache from settings.

    Returns None if Redis is disabled in config or if the master is
    unreachable at startup (graceful degradation — the app keeps working
    without cache in both cases).
    """
    if not s.redis_enabled:
        logger.info("Redis caching disabled (REDIS_ENABLED=false)")
        return None

    replica_specs = _parse_replica_specs(s.redis_replica_hosts)
    cache = build_redis_cache(
        master_host=s.redis_master_host,
        master_port=s.redis_master_port,
        replica_specs=replica_specs,
        password=s.redis_password,
        db=s.redis_db,
        socket_timeout=s.redis_socket_timeout,
        tls=s.redis_tls,
    )

    if cache.ping_master():
        replicas_info = f"{len(replica_specs)} replica(s)" if replica_specs else "no replicas"
        logger.info(
            "Redis connected — master=%s:%d  %s",
            s.redis_master_host,
            s.redis_master_port,
            replicas_info,
        )
        return cache

    logger.warning(
        "Redis master at %s:%d is unreachable — running without cache",
        s.redis_master_host,
        s.redis_master_port,
    )
    return None


def _mount_routes(app: FastAPI, api_prefix: str) -> None:
    p = api_prefix.rstrip("/")
    app.include_router(aarti_router.router, prefix=f"{p}/god/aartis", tags=["Aarti"])
    app.include_router(chalisa_router.router, prefix=f"{p}/god/chalisas", tags=["Chalisa"])
    app.include_router(stotram_router.router, prefix=f"{p}/god/stotram", tags=["Stotram"])
    app.include_router(mantra_router.router, prefix=f"{p}/god/mantras", tags=["Mantra"])
    app.include_router(gita_router.router, prefix=f"{p}/scriptures/gita", tags=["Gita"])
    app.include_router(ramayana_router.router, prefix=f"{p}/scriptures/ramayana", tags=["Ramayana"])
    app.include_router(mahabharata_router.router, prefix=f"{p}/scriptures/mahabharata", tags=["Mahabharata"])
    app.include_router(veda.router, prefix=f"{p}/vedas", tags=["Vedas"])
    app.include_router(search.router, prefix=f"{p}/search", tags=["Search"])
    app.include_router(astro.router, prefix=f"{p}/astro", tags=["Astro"])
    app.include_router(panchang_router.router, prefix=f"{p}/panchang", tags=["Panchang"])


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = httpx.Timeout(
        settings.webclient_timeout_read,
        connect=settings.webclient_timeout_connect,
        write=settings.webclient_timeout_write,
    )
    cache = _build_cache(settings)
    async with httpx.AsyncClient(
        timeout=timeout,
        headers={"Accept": "application/json"},
        follow_redirects=True,
    ) as client:
        app.state.settings = settings
        app.state.services = build_services(client, settings, cache)
        yield


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Mann Mandir Backend",
    description="REST API for Hindu spiritual content — Aarti, Chalisa, Gita, Vedas, and more",
    version=__version__,
    lifespan=lifespan,
)

_mount_routes(app, settings.api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)


@app.get("/")
async def root():
    return {"status": "ok", "service": "mann-mandir-backend", "version": __version__}


@app.get("/health_status", tags=["Health"])
async def health_status():
    return {"status": "up"}


@app.exception_handler(ResourceNotFoundError)
async def handle_not_found(_: Request, exc: ResourceNotFoundError):
    body = {
        "success": False,
        "errorDetail": {"code": "NOT_FOUND", "message": str(exc)},
    }
    return JSONResponse(status_code=404, content=body)


@app.exception_handler(ValueError)
async def handle_value_error(_: Request, exc: ValueError):
    body = {
        "success": False,
        "errorDetail": {"code": "BAD_REQUEST", "message": str(exc)},
    }
    return JSONResponse(status_code=400, content=body)


@app.exception_handler(Exception)
async def handle_generic(_: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    body = {
        "success": False,
        "errorDetail": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
    }
    return JSONResponse(status_code=500, content=body)
