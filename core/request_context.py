from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from starlette.requests import Request

from constants.api import (
    DEFAULT_RESOURCE_NAME,
    IDENTIFIER_QUERY_KEYS,
    PATH_RESOURCES,
    UNKNOWN_IDENTIFIER,
)

current_request: ContextVar[Optional[Request]] = ContextVar(
    "current_request", default=None
)


def resource_from_path(path: str) -> str:
    for suffix, name in PATH_RESOURCES:
        if suffix in path:
            return name
    return DEFAULT_RESOURCE_NAME


def identifier_from_request() -> tuple[str, str]:
    request = current_request.get()
    if request is None:
        return DEFAULT_RESOURCE_NAME, UNKNOWN_IDENTIFIER
    resource = resource_from_path(request.url.path)
    for key in IDENTIFIER_QUERY_KEYS:
        value = request.query_params.get(key)
        if value and value.strip():
            return resource, value.strip()
    parts = [part for part in request.url.path.split("/") if part]
    ident = parts[-1] if parts else UNKNOWN_IDENTIFIER
    return resource, ident
