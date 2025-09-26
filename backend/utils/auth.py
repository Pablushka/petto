from pydantic import BaseModel
from fastapi import Body
from typing import Union, Annotated
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas.users import LoginRequest, UserOut
from typing_extensions import Annotated, Doc

# Secret key for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

REFRESH_TOKEN_EXPIRE_DAYS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/OAuth2")


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


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    from models import User
    import json
    try:
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
        print(f"JWTError in get_current_user: {e}")
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
        print(f"JWTError in verify_refresh_token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
