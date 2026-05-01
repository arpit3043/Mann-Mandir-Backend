from __future__ import annotations

from enum import Enum
from typing import Optional


class ContentDomain(str, Enum):
    GOD = "god"
    SCRIPTURES = "scriptures"
    VEDAS = "vedas"
    SEARCH = "search"


def parse_content_domain(value: Optional[str]) -> Optional[ContentDomain]:
    if value is None or not str(value).strip():
        return None
    v = value.strip().lower()
    for d in ContentDomain:
        if d.value == v or d.name.lower() == v:
            return d
    raise ValueError(f"Unknown domain: {value}")
