
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    full_address: str
    recovery_bounty: Optional[float] = None


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    full_address: str
    recovery_bounty: Optional[float] = None
    hash: str
