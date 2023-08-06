from collections import deque
from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy.orm import Session

RepoData = TypeVar("RepoData")


class NoContextError(Exception):
    pass


class BaseRepo(Generic[RepoData]):
    def __init__(
        self,
        session: Session,
    ):
        self._session = session
        self._context_stack: deque[RepoData] = deque()

    @property
    def is_empty(self) -> bool:
        return not self._context_stack

    def status(self) -> RepoData:
        self._session.flush()

        return self.get()

    def apply(self) -> RepoData:
        result = self.get()
        self._session.commit()

        return result

    def get(self) -> RepoData:
        result = self._context_stack.pop()

        if result is None:
            raise NoContextError

        return result

    def first(self) -> RepoData | None:
        return self._context_stack.pop()

    def _append_context(self, context: RepoData) -> None:
        self._context_stack.append(context)
