from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from models import Pet, User
from utils.auth import get_current_user
from services.pdf_generator import get_pdf_generator
from pathlib import Path
from io import BytesIO

router = APIRouter(prefix="/api", tags=["Flyers"])

templates_dir = Path(__file__).resolve().parent.parent / \
    "static" / "flyers_templates"


def list_available_templates() -> list[str]:
    return sorted(
        template_file.stem
        for template_file in templates_dir.glob("*.html")
        if template_file.is_file()
    )


# Initialize templates
templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/flyers/templates")
async def get_flyer_templates(
    current_user: User = Depends(get_current_user)
):
    """List available flyer templates from backend static storage."""
    return {"templates": list_available_templates()}


@router.get("/flyers/{pet_id}", response_class=HTMLResponse)
async def generate_flyer_html(
    request: Request,
    pet_id: int,
    template: str = "old_west",
    print_mode: str = "color",
    current_user: User = Depends(get_current_user)
):
    """
    Generate an HTML flyer for a lost pet that can be printed or saved as PDF.
    """
    pet = await Pet.get_or_none(id=pet_id).prefetch_related("owner")
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if template not in list_available_templates():
        raise HTTPException(status_code=404, detail="Template not found")

    # Check if user owns the pet or is admin
    if pet.owner.id != current_user.id:
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
        "pet_age": "",
        "pet_breed": pet.breed or "",
        "pet_gender": pet.gender or "",
        "pet_last_seen_date": pet.last_seen_date.isoformat() if pet.last_seen_date else "",
        "pet_last_seen_geo": pet.last_seen_geo or "",
        "pet_distinctive1": pet.distinctive1 or "",
        "pet_distinctive2": pet.distinctive2 or "",
        "pet_distinctive3": pet.distinctive3 or "",
        "pet_distinctive4": pet.distinctive4 or "",
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
        "show_reward": bool(pet.owner.recovery_bounty),
        "print_mode": print_mode,
        "pet_id": pet.id
    }

    return templates.TemplateResponse(f"{template}.html", {
        "request": request,
        **template_data
    })


@router.get("/flyers/{pet_id}/pdf")
async def generate_flyer_pdf(
    request: Request,
    pet_id: int,
    format: str = "a4",
    orientation: str = "portrait",
    color_mode: str = "color",
    quality: str = "high",
    current_user: User = Depends(get_current_user)
):
    """
    Generate a PDF flyer for a lost pet using Chrome engine.
    """
    pet = await Pet.get_or_none(id=pet_id).prefetch_related("owner")
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Check if user owns the pet or is admin
    if pet.owner.id != current_user.id:
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
        "pet_age": "",
        "pet_breed": pet.breed or "",
        "pet_gender": pet.gender or "",
        "pet_last_seen_date": pet.last_seen_date.isoformat() if pet.last_seen_date else "",
        "pet_last_seen_geo": pet.last_seen_geo or "",
        "pet_distinctive1": pet.distinctive1 or "",
        "pet_distinctive2": pet.distinctive2 or "",
        "pet_distinctive3": pet.distinctive3 or "",
        "pet_distinctive4": pet.distinctive4 or "",
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
        "show_reward": bool(pet.owner.recovery_bounty),
        "print_mode": color_mode,
        "pet_id": pet.id
    }

    # Get PDF generator and create PDF
    pdf_generator = get_pdf_generator()

    try:
        pdf_bytes = await pdf_generator.generate_flyer_pdf(
            pet_data=template_data,
            format=format,
            orientation=orientation,
            color_mode=color_mode,
            quality=quality
        )

        # Return PDF as streaming response
        filename = f"lost_pet_flyer_{pet.name}_{pet.id}.pdf"
        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }

        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers=headers
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )
