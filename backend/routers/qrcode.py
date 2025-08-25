from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import qrcode
import io
from models import Pet, User

router = APIRouter(tags=["QR Code"])


@router.get("/qrcode/{pet_id}")
async def generate_qr_code(pet_id: int):
    """
    Generate a QR code for a pet by pet ID.
    Returns a PNG image.
    http GET :8000/qrcode/1
    """
    pet = await Pet.get_or_none(id=pet_id).prefetch_related("owner")
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    buf = pet.generate_qr_code()
    return StreamingResponse(buf, media_type="image/png")


@router.post("/qrcode/scan/{scan_id}")
async def scan_qr_code(scan_id: str):
    """
    Record a QR code scan for a pet and owner.
    Sample scan_id: "<owner_hash>|<pet_id>"
    http POST :8000/qrcode/scan/abc123|1
    """
    try:
        owner_hash, pet_id_str = scan_id.split("|", 1)
        pet_id = int(pet_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid scan_id format")

    owner = await User.get_or_none(hash=owner_hash)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    pet = await Pet.get_or_none(id=pet_id, owner_id=owner.id)
    if not pet:
        raise HTTPException(
            status_code=404, detail="Pet not found for this owner")

    # In a real application, you would send an email notification here.
    print(f"QR code for pet {pet.name} (owner: {owner.email}) was scanned.")

    return {"message": "Scan recorded successfully"}
