from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str


class PaginationMeta(BaseModel):
    page: int
    size: int
    totalElements: int
    totalPages: int
    hasNext: bool
    hasPrevious: bool


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    errorDetail: Optional[ErrorDetail] = Field(default=None, serialization_alias="errorDetail")
    paginationMeta: Optional[PaginationMeta] = Field(
        default=None, serialization_alias="paginationMeta"
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"populate_by_name": True}

    @staticmethod
    def ok_data(data: T, pagination: Optional[PaginationMeta] = None) -> "ApiResponse[T]":
        return ApiResponse(success=True, data=data, paginationMeta=pagination)

    @staticmethod
    def ok_message(data: T, message: str) -> "ApiResponse[T]":
        return ApiResponse(success=True, message=message, data=data)

    @staticmethod
    def error(code: str, message: str) -> "ApiResponse[Any]":
        return ApiResponse(success=False, errorDetail=ErrorDetail(code=code, message=message))


def meta_from_totals(page: int, size: int, total: int) -> PaginationMeta:
    import math

    if size <= 0:
        size = 20
    total_pages = int(math.ceil(total / size)) if total > 0 else 0
    has_next = page < total_pages - 1 if total_pages > 0 else False
    return PaginationMeta(
        page=page,
        size=size,
        totalElements=total,
        totalPages=total_pages,
        hasNext=has_next,
        hasPrevious=page > 0,
    )
