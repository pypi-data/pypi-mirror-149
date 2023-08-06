from pydantic import BaseModel


class AuthSettings(BaseModel):
    secrete_key: str = "secret_key"
    algorithm: str = "RS256"
