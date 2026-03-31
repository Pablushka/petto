from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import date
from models import PetType, PetStatus


class PetBase(BaseModel):
    name: str = Field(..., max_length=255)
    pet_type: PetType
    breed: Optional[str] = Field(None, max_length=100)
    last_seen_date: Optional[date] = None
    last_seen_geo: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=32)
    distinctive1: Optional[str] = Field(None, max_length=100)
    distinctive2: Optional[str] = Field(None, max_length=100)
    distinctive3: Optional[str] = Field(None, max_length=100)
    distinctive4: Optional[str] = Field(None, max_length=100)
    picture: str = Field(..., max_length=1024)
    notes: str
    status: PetStatus = PetStatus.AT_HOME
    # Optional list representation (outgoing only normally). For create/update we allow passing pictures.
    pictures: Optional[List[str]] = None


class PetCreate(PetBase):
    # owner_id is now optional and ignored if provided; router derives it from auth.
    # Retained only for backward compatibility with older clients.
    owner_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_pictures(cls, values):  # type: ignore
        pics = values.pictures
        if pics:
            if len(pics) > 5:
                raise ValueError("Maximum 5 pictures allowed")
            # Basic length constraint reuse
            for p in pics:
                if len(p) > 1024:
                    raise ValueError("Picture path too long (max 1024)")
        return values


class PetUpdate(BaseModel):
    # All fields optional to allow partial updates if desired (currently PUT expects full entity, but this is flexible)
    name: Optional[str] = Field(None, max_length=255)
    pet_type: Optional[PetType] = None
    breed: Optional[str] = Field(None, max_length=100)
    last_seen_date: Optional[date] = None
    last_seen_geo: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=32)
    distinctive1: Optional[str] = Field(None, max_length=100)
    distinctive2: Optional[str] = Field(None, max_length=100)
    distinctive3: Optional[str] = Field(None, max_length=100)
    distinctive4: Optional[str] = Field(None, max_length=100)
    picture: Optional[str] = Field(None, max_length=1024)
    notes: Optional[str] = None
    status: Optional[PetStatus] = None
    owner_id: Optional[int] = None  # See TODO above
    pictures: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_pictures(cls, values):  # type: ignore
        pics = values.pictures
        if pics:
            if len(pics) > 5:
                raise ValueError("Maximum 5 pictures allowed")
            for p in pics:
                if len(p) > 1024:
                    raise ValueError("Picture path too long (max 1024)")
        return values


class PetOut(PetBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Pydantic v2: allow ORM object attr reading


# Backwards compatibility exports (old names)
PetIn = PetCreate


# Serializer helpers
def serialize_pet(p) -> PetOut:
    """Convert a Pet ORM instance to PetOut.

    Accepts a Tortoise Pet model (duck-typed) and constructs a PetOut using explicit fields
    to avoid accidental leakage of internal attributes.
    """
    pictures_ordered: List[str] = [
        val for val in [
            getattr(p, "picture", None),
            getattr(p, "picture2", None),
            getattr(p, "picture3", None),
            getattr(p, "picture4", None),
            getattr(p, "picture5", None),
        ] if val
    ]
    primary = pictures_ordered[0] if pictures_ordered else getattr(
        p, "picture", "")
    return PetOut.model_validate(
        {
            "id": p.id,
            "owner_id": p.owner_id,
            "name": p.name,
            "pet_type": p.pet_type,
            "breed": getattr(p, "breed", None),
            "last_seen_date": getattr(p, "last_seen_date", None),
            "last_seen_geo": getattr(p, "last_seen_geo", None),
            "gender": getattr(p, "gender", None),
            "distinctive1": getattr(p, "distinctive1", None),
            "distinctive2": getattr(p, "distinctive2", None),
            "distinctive3": getattr(p, "distinctive3", None),
            "distinctive4": getattr(p, "distinctive4", None),
            "picture": primary,
            "notes": p.notes,
            "status": p.status,
            "pictures": pictures_ordered or None,
        }
    )


def serialize_pet_list(pets) -> list[PetOut]:
    return [serialize_pet(p) for p in pets]
