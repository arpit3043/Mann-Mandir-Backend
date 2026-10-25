from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from starlette.requests import Request

current_request: ContextVar[Optional[Request]] = ContextVar("current_request", default=None)

_PATH_RESOURCES = (
    ("/god/aartis", "Aarti"),
    ("/god/chalisas", "Chalisa"),
    ("/god/stotram", "Stotram"),
    ("/god/mantras", "Mantra"),
    ("/vedas/mantras", "Mantra"),
    ("/vedas/upanishads", "Upanishad"),
    ("/vedas/rig", "Rig Veda"),
    ("/vedas", "Veda"),
    ("/scriptures/gita", "Gita"),
    ("/scriptures/ramayana", "Ramayana"),
    ("/scriptures/mahabharata", "Mahabharata"),
    ("/search", "Search"),
    ("/panchang", "Panchang"),
    ("/astro", "Astro"),
)


def resource_from_path(path: str) -> str:
    for suffix, name in _PATH_RESOURCES:
        if suffix in path:
            return name
    return "Result"


def identifier_from_request() -> tuple[str, str]:
    request = current_request.get()
    if request is None:
        return "Result", "requested data"
    resource = resource_from_path(request.url.path)
    for key in ("deity", "query", "q", "poet", "sign", "name"):
        value = request.query_params.get(key)
        if value and value.strip():
            return resource, value.strip()
    parts = [part for part in request.url.path.split("/") if part]
    ident = parts[-1] if parts else "requested data"
    return resource, ident
