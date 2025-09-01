from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from models import User
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user
from schemas.users import UserCreate, UserOut, UserRegister, PasswordRecoveryRequest, PasswordResetRequest, LoginRequest

router = APIRouter(prefix="/api", tags=["Users"])

# User registration endpoint


@router.post("/register", response_model=UserOut)
async def register(user: UserRegister):
    """
    Register a new user.
    Request body: {first_name, last_name, email, phone, full_address, recovery_bounty, password}
    Response: UserOut
    """
    existing_user = await User.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    user_obj = await User.create(**user_data)
    return user_obj

# Password recovery request endpoint


@router.post("/password-recovery")
async def password_recovery(request: PasswordRecoveryRequest):
    """
    Request password recovery for a user by email.
    Returns a recovery token (stub).
    """
    user = await User.get_or_none(email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Here you would send a recovery email with a token (stubbed)
    token = create_access_token(
        {"sub": str(user.id)}, expires_delta=timedelta(minutes=15))
    # send_email(user.email, token)

    return {"message": "Recovery email sent (stub)", "token": token}

# Password reset endpoint


@router.post("/password-reset")
async def password_reset(request: PasswordResetRequest):
    """
    Reset user password using a recovery token.
    Request body: {token, new_password}
    """
    # Decode token and get user id (stubbed, should verify token)
    try:
        from jose import jwt
        from utils.auth import SECRET_KEY, ALGORITHM
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        user = UserOut(**(payload.get("sub")))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = await User.get_or_none(id=user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = get_password_hash(request.new_password)
    await user.save(update_fields=["password"])
    return {"message": "Password reset successful"}


@router.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    """
    Create a new user (admin/system use).
    Request body: {first_name, last_name, email, phone, full_address, recovery_bounty, password}
    Response: UserOut
    """
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
        "password": "yourpassword"
    }
    http POST :8000/users/ first_name=John last_name=Doe email=john@example.com phone=1234567890 full_address="123 Main St, City" recovery_bounty:=50.0
    """
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password
    user_obj = await User.create(**user_data)
    return user_obj
# Login route


@router.post("/login")
async def loginJson(request: LoginRequest):
    """
    Authenticate user and return JWT token.
    Request body: {email, password}
    Response: {access_token, token_type}
    """
    user = await User.get_or_none(email=request.email)
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        # "phone": user.phone,
        # "full_address": user.full_address,
        # "recovery_bounty": float(user.recovery_bounty) if user.recovery_bounty is not None else None,
        # "hash": user.hash
    }
    import json
    user_json = json.dumps(user_data)
    access_token = create_access_token(
        data={"sub": user_json})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/OAuth2")
async def loginForm(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user using OAuth2 form data (legacy).
    Request body: form-data with username and password.
    Response: {access_token, token_type}
    """
    user = await User.get_or_none(email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user (requires authentication).
    """
    return current_user


@router.get("/users/", response_model=List[UserOut])
async def get_users(current_user: User = Depends(get_current_user)):
    """
    Get a list of all users (requires authentication).
    """
    """
    Get a list of all users.
    http GET :8000/users/
    """
    return await User.all()


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    """
    Get a user by ID (requires authentication).
    """
    """
    Get a user by ID.
    http GET :8000/users/1
    """
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, current_user: User = Depends(get_current_user)):
    """
    Update a user by ID (requires authentication).
    Request body: {first_name, last_name, email, phone, full_address, recovery_bounty, password}
    """
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
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    """
    Delete a user by ID (requires authentication).
    """
    """
    Delete a user by ID.
    http DELETE :8000/users/1
    """
    user_obj = await User.get_or_none(id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    await user_obj.delete()
    return {"message": "User deleted successfully"}
