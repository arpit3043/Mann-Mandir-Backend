from __future__ import annotations

from enum import Enum
from typing import Optional


class ContentDomain(str, Enum):
    GOD = "god"
    SCRIPTURES = "scriptures"
    VEDAS = "vedas"
    SEARCH = "search"


class SearchType(str, Enum):
    AARTI = "aarti"
    CHALISA = "chalisa"
    STOTRAM = "stotram"
    MANTRA = "mantra"
    GITA = "gita"
    VEDA = "veda"
    UPANISHAD = "upanishad"


def parse_content_domain(value: Optional[str]) -> Optional[ContentDomain]:
    if value is None or not str(value).strip():
        return None
    v = value.strip().lower()
    for domain in ContentDomain:
        if domain.value == v or domain.name.lower() == v:
            return domain
    raise ValueError(f"Unknown domain: {value}")
