import os
import uuid
from typing import Literal
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from models import User
from utils.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Upload"])

BASE_STATIC_SUBDIR = "uploads"

# Resolve absolute path relative to this file: ../static/uploads
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../static")
UPLOAD_DIR = os.path.normpath(os.path.join(STATIC_ROOT, BASE_STATIC_SUBDIR))
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
ALLOWED_CONTENT_TYPES: set[str] = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _validate_image_file(upload: UploadFile):
    if upload.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")
    _, ext = os.path.splitext(upload.filename or "")
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file extension")


@router.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a single image file and return a relative static URL.

    Security: requires authentication; future enhancement could add per-user quota.
    Response shape matches frontend expectation: { "url": "/static/uploads/<file>" }
    """
    _validate_image_file(image)
    # Read file content and validate size
    content = await image.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = os.path.splitext(image.filename or "")[-1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, str(current_user.id))
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    dest_file = os.path.join(dest_path, f"{filename}")
    with open(dest_file, "wb") as f:
        f.write(content)

    base = f"static/{BASE_STATIC_SUBDIR}/"
    # if base not exits, create the directory

    url = f"{base}{current_user.id}/{filename}"
    
    # Return path relative to static mount
    return JSONResponse({"url": url})
