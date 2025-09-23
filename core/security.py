from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from .config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str | int, expires_minutes: Optional[int] = None, extra_claims: Optional[dict[str, Any]] = None) -> str:
    settings = get_settings()
    expire_delta = timedelta(minutes=expires_minutes or settings.jwt_access_token_expires_minutes)
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": datetime.now(timezone.utc) + expire_delta}
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


