from pydantic import BaseModel

from popug_sdk.schemas.response_schema import get_response_schema


class Hello(BaseModel):
    hello: str | None = None


if __name__ == "__main__":
    schema = get_response_schema(Hello)
    res = schema(**{"result": {"hello": "world"}})
    print(res.json())
