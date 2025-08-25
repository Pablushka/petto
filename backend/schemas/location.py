from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    pet_id: int
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
