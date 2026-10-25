from __future__ import annotations

import math
from typing import List, Optional, TypeVar

from constants.api import DEFAULT_PAGE_SIZE, JAVA_MAX_INT

T = TypeVar("T")


def paginate(source: Optional[List[T]], page: int, size: int) -> List[T]:
    if not source:
        return []
    if size == JAVA_MAX_INT:
        return list(source)
    start = min(page * size, len(source))
    end = min(start + size, len(source))
    return source[start:end]


def pagination_meta(page: int, size: int, total: int) -> dict:
    if size <= 0:
        size = DEFAULT_PAGE_SIZE
    total_pages = max(1, math.ceil(total / size)) if total else 0
    has_next = page < total_pages - 1 if total_pages else False
    has_previous = page > 0
    return {
        "page": page,
        "size": size,
        "totalElements": total,
        "totalPages": total_pages,
        "hasNext": has_next,
        "hasPrevious": has_previous,
    }
