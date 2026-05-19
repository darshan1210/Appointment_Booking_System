"""Authentication schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# ─── Token Schemas ───

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None
    exp: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str