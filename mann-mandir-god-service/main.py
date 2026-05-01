from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from mann_mandir import __version__
from api.deps import build_services
from api.routers import scripture, veda
from api.routers import god, search
from core.config import Settings
from core.exceptions import ResourceNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


def _mount_routes(app: FastAPI, api_prefix: str) -> None:
    p = api_prefix.rstrip("/")
    app.include_router(god.router, prefix=f"{p}/god", tags=["God"])
    app.include_router(scripture.router, prefix=f"{p}/scriptures", tags=["Scriptures"])
    app.include_router(veda.router, prefix=f"{p}/vedas", tags=["Vedas"])
    app.include_router(veda.router, prefix=f"{p}/veda", tags=["Vedas"])
    app.include_router(search.router, prefix=f"{p}/search", tags=["Search"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = httpx.Timeout(
        settings.webclient_timeout_read,
        connect=settings.webclient_timeout_connect,
        write=settings.webclient_timeout_write,
    )
    async with httpx.AsyncClient(
        timeout=timeout,
        headers={"Accept": "application/json"},
        follow_redirects=True,
    ) as client:
        app.state.settings = settings
        app.state.services = build_services(client, settings)
        yield


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
