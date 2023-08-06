from typing import (
    Any,
    Union,
)

ResultT = Union[list[dict[str, Any]], dict[str, Any]]


def get_response_data(
    result: ResultT,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {"result": result} | (meta or {})
