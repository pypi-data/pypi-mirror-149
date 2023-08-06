from typing import TypedDict

from fastapi import Query

from popug_sdk.constants import DEFAULT_PAGE_SIZE


class PaginationDict(TypedDict):
    page: int
    page_size: int
    count: int


class PaginationMetaDict(TypedDict):
    pagination: PaginationDict


class BasePagination:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    ) -> None:
        self._page = page
        self._page_size = page_size

    def get_params(self, count: int) -> PaginationMetaDict:
        raise NotImplementedError


class PagePagination(BasePagination):
    def get_params(self, count: int) -> PaginationMetaDict:
        return {
            "pagination": {
                "page": self._page,
                "page_size": self._page_size,
                "count": count,
            }
        }
