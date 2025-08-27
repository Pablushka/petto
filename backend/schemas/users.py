from typing import Optional
from pydantic import BaseModel


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    full_address: str
    recovery_bounty: Optional[float] = None
    password: str


class PasswordRecoveryRequest(BaseModel):
    email: str


class PasswordResetRequest(BaseModel):
    token: str
    new_password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    full_address: str
    recovery_bounty: Optional[float] = None
    password: str


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    full_address: str
    recovery_bounty: Optional[float] = None
    hash: str
