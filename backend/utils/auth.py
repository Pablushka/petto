from pydantic import BaseModel
from fastapi import Body
from typing import Union, Annotated
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from schemas.users import LoginRequest, UserOut
from typing_extensions import Annotated, Doc
from config import settings
import logging

# Get security logger for authentication events
security_logger = logging.getLogger("security")

# JWT Configuration from environment
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

# Cookie settings shared across login/refresh flows
ACCESS_TOKEN_COOKIE_NAME = "access_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
COOKIE_PATH = "/"
COOKIE_SAMESITE = "strict" if settings.environment == "production" else "lax"
# Dynamic security based on environment
COOKIE_SECURE = settings.environment == "production"


def _access_cookie_max_age() -> int:
    return ACCESS_TOKEN_EXPIRE_MINUTES * 60


def _refresh_cookie_max_age() -> int:
    return REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Persist access/refresh tokens on the response as HTTP-only cookies."""
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=_access_cookie_max_age(),
        path=COOKIE_PATH,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=_refresh_cookie_max_age(),
        path=COOKIE_PATH,
    )


def clear_auth_cookies(response: Response) -> None:
    """Remove auth cookies from the response."""
    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME, path=COOKIE_PATH)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME, path=COOKIE_PATH)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/OAuth2")
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/api/login/OAuth2", auto_error=False)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, token: str | None = Depends(oauth2_scheme_optional)):
    from models import User
    import json
    try:
        if not token:
            token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data_raw = payload.get("sub")
        # 'sub' can be:
        # - a JSON string containing a dict with 'id' (e.g. login path)
        # - a string with a numeric id (e.g. create_access_token with user id)
        # - an int (if token was created with a numeric sub)
        # Be defensive when parsing.

        def _extract_user_id(raw):
            # raw may be dict, int, or string
            if isinstance(raw, dict):
                return raw.get("id")
            if isinstance(raw, int):
                return raw
            if isinstance(raw, str):
                # try JSON decode
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        return parsed.get("id")
                    if isinstance(parsed, (int, str)) and str(parsed).isdigit():
                        return int(parsed)
                    return parsed
                except Exception:
                    # not JSON, maybe numeric string
                    if raw.isdigit():
                        return int(raw)
                    return raw

        user_id = _extract_user_id(user_data_raw)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        security_logger.warning("JWT validation failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def verify_refresh_token(refresh_token: str):
    import json
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data_raw = payload.get("sub")
        # reuse same extraction logic as above

        def _extract_user_id(raw):
            if isinstance(raw, dict):
                return raw.get("id")
            if isinstance(raw, int):
                return raw
            if isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        return parsed.get("id")
                    if isinstance(parsed, (int, str)) and str(parsed).isdigit():
                        return int(parsed)
                    return parsed
                except Exception:
                    if raw.isdigit():
                        return int(raw)
                    return raw

        user_id = _extract_user_id(user_data_raw)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError as e:
        security_logger.warning("Refresh token validation failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
