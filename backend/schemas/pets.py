from pydantic import BaseModel


class PetCreate(BaseModel):
    name: str
    picture: str
    notes: str
    pet_type: str
    owner_id: int


class PetOut(BaseModel):
    id: int
    name: str
    picture: str
    notes: str
    pet_type: str
    owner_id: int
