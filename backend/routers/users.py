from fastapi import APIRouter, HTTPException
from typing import List
from models import User
from schemas.users import UserCreate, UserOut

router = APIRouter(tags=["Users"])


@router.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    """
    Create a new user.
    Sample JSON for httpie:
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "full_address": "123 Main St, City",
        "recovery_bounty": 50.0
    }
    http POST :8000/users/ first_name=John last_name=Doe email=john@example.com phone=1234567890 full_address="123 Main St, City" recovery_bounty:=50.0
    """
    user_obj = await User.create(**user.dict())
    return user_obj


@router.get("/users/", response_model=List[UserOut])
async def get_users():
    """
    Get a list of all users.
    http GET :8000/users/
    """
    return await User.all()


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    """
    Get a user by ID.
    http GET :8000/users/1
    """
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate):
    """
    Update a user by ID.
    Sample JSON for httpie:
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone": "9876543210",
        "full_address": "456 Elm St, City",
        "recovery_bounty": 75.0
    }
    http PUT :8000/users/1 first_name=Jane last_name=Smith email=jane@example.com phone=9876543210 full_address="456 Elm St, City" recovery_bounty:=75.0
    """
    user_obj = await User.get_or_none(id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    await user_obj.update_from_dict(user.dict()).save()
    return user_obj


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    """
    Delete a user by ID.
    http DELETE :8000/users/1
    """
    user_obj = await User.get_or_none(id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    await user_obj.delete()
    return {"message": "User deleted successfully"}
