from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Pet, User
from utils.auth import get_current_user
import os

router = APIRouter(prefix="/api", tags=["Flyers"])

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(
    current_dir, "..", "..", "apps", "frontend", "src", "lib", "flyers_templates")

# Initialize templates
templates = Jinja2Templates(directory=templates_dir)


@router.get("/flyers/{pet_id}", response_class=HTMLResponse)
async def generate_flyer_html(
    request: Request,
    pet_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Generate an HTML flyer for a lost pet that can be printed or saved as PDF.
    """
    pet = await Pet.get_or_none(id=pet_id).prefetch_related("owner")
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Check if user owns the pet or is admin
    if pet.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only generate flyers for your own pets")

    # Get base URL for absolute URLs
    base_url = f"{request.url.scheme}://{request.url.hostname}"
    if request.url.port and request.url.port != (443 if request.url.scheme == 'https' else 80):
        base_url += f":{request.url.port}"

    # Function to resolve image URLs
    def resolve_image_url(url: str) -> str:
        if url.startswith('http'):
            return url
        # Remove leading slashes and construct absolute URL
        cleaned = url.lstrip('/')
        return f"{base_url}/{cleaned}"

    # Prepare template data
    template_data = {
        "pet_name": pet.name,
        "pet_type": pet.pet_type,
        "pet_age": "",  # These would come from additional fields if added to model
        "pet_breed": "",
        "pet_color": "",
        "pet_gender": "",
        "pet_last_seen": "",
        "pet_location": "",
        "pet_description": pet.notes or "",
        "pet_picture": resolve_image_url(pet.picture) if pet.picture else "",
        "pet_picture2": resolve_image_url(pet.picture2) if pet.picture2 else "",
        "pet_picture3": resolve_image_url(pet.picture3) if pet.picture3 else "",
        "pet_picture4": resolve_image_url(pet.picture4) if pet.picture4 else "",
        "pet_picture5": resolve_image_url(pet.picture5) if pet.picture5 else "",
        "qr_code_url": f"{base_url}/api/qrcode/{pet.id}",
        "owner_name": f"{pet.owner.first_name} {pet.owner.last_name}",
        "owner_phone": pet.owner.phone,
        "owner_email": pet.owner.email,
        "owner_address": pet.owner.full_address,
        "reward_amount": f"${pet.owner.recovery_bounty}" if pet.owner.recovery_bounty else "",
        "show_reward": "block" if pet.owner.recovery_bounty else "none",
        "pet_id": pet.id
    }

    return templates.TemplateResponse("lost_pet_flyer.html", {
        "request": request,
        **template_data
    })
