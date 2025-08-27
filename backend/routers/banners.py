from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from models import Pet, User
from utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Pets"])


@router.get("/banners/{pet_id}")
async def generate_banner(pet_id: int, current_user: User = Depends(get_current_user)):
    pet = await Pet.get_or_none(id=pet_id).prefetch_related("owner")
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Create a blank image
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)

    # Add title
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font_title = ImageFont.load_default()
    d.text((400, 50), "LOST PET", font=font_title, fill=(0, 0, 0), anchor="ms")

    # Add pet name
    try:
        font_name = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_name = ImageFont.load_default()
    d.text((400, 120), pet.name, font=font_name, fill=(0, 0, 0), anchor="ms")

    # Add pet picture
    try:
        response = requests.get(pet.picture, stream=True)
        response.raise_for_status()
        pet_img = Image.open(response.raw)
        pet_img.thumbnail((400, 300))
        img.paste(pet_img, (200, 150))
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

    # Add contact information
    try:
        font_contact = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_contact = ImageFont.load_default()
    contact_info = f"Owner: {pet.owner.first_name} {pet.owner.last_name}\nPhone: {pet.owner.phone}\nEmail: {pet.owner.email}"
    d.text((400, 500), contact_info, font=font_contact,
           fill=(0, 0, 0), anchor="ms")

    # Save image to a buffer
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
