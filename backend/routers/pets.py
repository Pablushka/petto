from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import Pet, User
from utils.auth import get_current_user
from schemas.pets import (
    PetCreate,
    PetOut,
    PetUpdate,
    PetIn,  # backward compatibility
    serialize_pet,
    serialize_pet_list,
)

router = APIRouter(prefix="/api", tags=["Pets"])


@router.post("/pets/", response_model=PetOut)
async def create_pet(pet: PetCreate, current_user: User = Depends(get_current_user)):
    """
    Create a new pet.

    Sample JSON (owner_id omitted – derived from auth, can submit either picture or pictures array):
    {
        "name": "Rex",
        "pet_type": "Dog",
        "pictures": ["https://example.com/rex1.jpg", "https://example.com/rex2.jpg"],
        "notes": "Brown dog, friendly",
        "status": "lost"
    }
    http POST :8000/pets/ name=Rex pet_type=Dog pictures:='["https://example.com/rex1.jpg"]' notes="Brown dog, friendly" status=lost
    """
    # Override owner_id with authenticated user for security (ignore provided owner_id if mismatch)
    owner_id = current_user.id
    pet_data = pet.model_dump()
    pet_data["owner_id"] = owner_id
    pictures = pet_data.pop("pictures", None)
    if pictures:
        # Map array to columns
        pet_data["picture"] = pictures[0]
        extras = pictures[1:]
        column_names = ["picture2", "picture3", "picture4", "picture5"]
        for col, val in zip(column_names, extras):
            pet_data[col] = val
    pet_obj = await Pet.create(**pet_data)
    return serialize_pet(pet_obj)


@router.get("/pets/", response_model=List[PetOut])
async def get_pets(current_user: User = Depends(get_current_user)):
    """
    Get a list of all pets.
    http GET :8000/pets/
    """
    # Fetch all pets for the current user and serialize explicitly
    pets = await Pet.filter(owner_id=current_user.id).all()
    return serialize_pet_list(pets)


@router.get("/pets/{pet_id}", response_model=PetOut)
async def get_pet(pet_id: int, current_user: User = Depends(get_current_user)):
    """
    Get a pet by ID.
    http GET :8000/pets/1
    """
    pet = await Pet.get_or_none(id=pet_id, owner_id=current_user.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return serialize_pet(pet)


@router.put("/pets/{pet_id}", response_model=PetOut)
async def update_pet(pet_id: int, pet: PetUpdate, current_user: User = Depends(get_current_user)):
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
    pet_obj = await Pet.get_or_none(id=pet_id, owner_id=current_user.id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    update_data = pet.model_dump(exclude_unset=True)
    pictures = update_data.pop("pictures", None)

    if pictures is not None:
        # Reset all columns then assign
        update_data["picture"] = pictures[0] if pictures else pet_obj.picture
        column_names = ["picture2", "picture3", "picture4", "picture5"]

        for col in column_names:
            update_data[col] = None
        extras = pictures[1:]
        for col, val in zip(column_names, extras):
            update_data[col] = val
            
    # Enforce ownership
    if "owner_id" in update_data:
        update_data["owner_id"] = current_user.id
    # Use queryset update to avoid partial instance save issues
    if update_data:
        await Pet.filter(id=pet_id, owner_id=current_user.id).update(**update_data)
    pet_obj = await Pet.get(id=pet_id)
    return serialize_pet(pet_obj)


@router.delete("/pets/{pet_id}", response_model=dict)
async def delete_pet(pet_id: int, current_user: User = Depends(get_current_user)):
    """
    Delete a pet by ID.
    http DELETE :8000/pets/1
    """
    pet_obj = await Pet.get_or_none(id=pet_id, owner_id=current_user.id)
    if not pet_obj:
        raise HTTPException(status_code=404, detail="Pet not found")
    await pet_obj.delete()
    return {"message": "Pet deleted successfully"}
