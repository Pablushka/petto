from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

from models import User
from utils.auth import get_current_user
router = APIRouter(prefix="/api/pet-location", tags=["Pet Location & QR"])

# Example in-memory store (replace with DB integration)
pet_scan_events = []


class PetScanEvent(BaseModel):
    pet_id: int
    user_id: int
    scan_location: Optional[str] = None
    scan_time: datetime = datetime.now(timezone.utc)
    qr_link: str


@router.post("/scan")
def record_pet_scan(event: PetScanEvent, request: Request, current_user: User = Depends(get_current_user)):
    """
    Record a pet scan event.
    Sample JSON for httpie:
    {
        "pet_id": 1,
        "user_id": 2,
        "scan_location": "Park Entrance",
        "qr_link": "https://doko.app/user-profile?hash=abc123"
    }
    http POST :8000/pet-location/scan pet_id:=1 user_id:=2 scan_location="Park Entrance" qr_link="https://doko.app/user-profile?hash=abc123"
    """
    # Save scan event (replace with DB logic)
    pet_scan_events.append(event.model_dump())
    # TODO: Notify owner by email (integrate email service)
    return {"message": "Scan recorded", "event": event}


@router.get("/pet/{pet_id}/qr-link")
async def get_qr_link(pet_id: int, current_user: User = Depends(get_current_user)):
    """
    Get the QR link for a pet by pet ID.
    http GET :8000/pet-location/pet/1/qr-link
    """
    # Fetch pet and owner's hash from DB
    from models import Pet, User
    pet = await Pet.get_or_none(id=pet_id).prefetch_related('owner')
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    owner = await User.get_or_none(id=pet.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    qr_link = f"https://doko.app/user-profile?hash={owner.hash}"
    return {"pet_id": pet_id, "qr_link": qr_link}


@router.get("/pet/{pet_id}/scans")
def get_pet_scans(pet_id: int, current_user: User = Depends(get_current_user)):
    scans = [e for e in pet_scan_events if e["pet_id"] == pet_id]
    return {"pet_id": pet_id, "scans": scans}
