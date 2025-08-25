from fastapi import APIRouter, HTTPException
from typing import List
from models import Pet, User
from schemas.pets import PetCreate, PetOut

router = APIRouter(tags=["Pets"])


@router.post("/pets/", response_model=PetOut)
async def create_pet(pet: PetCreate):
    """
    Create a new pet.
    Sample JSON for httpie:
    {
        "owner_id": 1,
        "name": "Rex",
        "pet_type": "Dog",
        "picture": "https://example.com/rex.jpg",
        "notes": "Brown dog, friendly"
    }
    http POST :8000/pets/ owner_id:=1 name=Rex pet_type=Dog picture="https://example.com/rex.jpg" notes="Brown dog, friendly"
    """
    owner = await User.get_or_none(id=pet.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    pet_obj = await Pet.create(**pet.model_dump())
    return pet_obj


@router.get("/pets/", response_model=List[PetOut])
async def get_pets():
    """
    Get a list of all pets.
    http GET :8000/pets/
    """
    return await Pet.all()


@router.get("/pets/{pet_id}", response_model=PetOut)
async def get_pet(pet_id: int):
    """
    Get a pet by ID.
    http GET :8000/pets/1
    """
    pet = await Pet.get_or_none(id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/pets/{pet_id}", response_model=PetOut)
async def update_pet(pet_id: int, pet: PetCreate):
    """
    Update a pet by ID.
        Sample JSON for httpie:
        {
            "owner_id": 1,
            "name": "Max",
            "pet_type": "Cat",
            "picture": "https://example.com/max.jpg",
            "notes": "Black cat, shy"
        }
        http PUT :8000/pets/1 owner_id:=1 name=Max pet_type=Cat picture="https://example.com/max.jpg" notes="Black cat, shy"
    """
    pet_obj = await Pet.get_or_none(id=pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Pet not found")
    owner = await User.get_or_none(id=pet.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    await pet_obj.update_from_dict(pet.model_dump()).save()
    return pet_obj


@router.delete("/pets/{pet_id}", response_model=dict)
async def delete_pet(pet_id: int):
    """
    Delete a pet by ID.
    http DELETE :8000/pets/1
    """
    pet_obj = await Pet.get_or_none(id=pet_id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Pet not found")
    await pet_obj.delete()
    return {"message": "Pet deleted successfully"}
