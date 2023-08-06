from typing import Any

import jwt
from fastapi import (
    Depends,
    HTTPException,
)
from jwt import PyJWTError
from starlette import status

from popug_sdk.auth.oauth_schema import oauth2_schema


def get_token_data(token: str = Depends(oauth2_schema)) -> dict[str, Any]:
    token = token.replace("Bearer ", "")

    secrete_key = "secret"
    algorithm = ...

    try:
        token_payload = jwt.decode(token, secrete_key, algorithms=algorithm)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return token_payload
