
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import mimetypes
from pathlib import Path

router = APIRouter()

# Mount static files (e.g., /static/style.css)
base_dir = Path(__file__).resolve().parent.parent / 'static'
uploads_dir = base_dir / 'uploads'
static_dir = base_dir
router.mount('/static', StaticFiles(directory=str(static_dir)), name='static')

# Set up Jinja2 templates (e.g., /templates/index.html)
templates_dir = base_dir / 'templates'
templates = Jinja2Templates(directory=str(templates_dir))


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the home page (index.html) from the templates directory.
    """
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/favicon.ico')
async def favicon():
    """Serve favicon. Prefer favicon.svg (vector) else fallback to any .ico present."""
    svg_path = static_dir / 'favicon.svg'
    if svg_path.is_file():
        return FileResponse(str(svg_path), media_type='image/svg+xml')
    ico_path = static_dir / 'favicon.ico'
    if ico_path.is_file():
        return FileResponse(str(ico_path), media_type='image/x-icon')
    raise HTTPException(status_code=404, detail='Favicon not found')


@router.get('/static/uploads/{user_id}/{filename}')
async def get_uploaded_image(user_id: str, filename: str):
    """Serve an uploaded image from the uploads directory.

    Security:
    - Prevent path traversal by resolving and ensuring the path stays within uploads_dir.
    - Only serve existing regular files.
    - Derive content-type via mimetypes (fallback to application/octet-stream).
    """
    requested_path = (uploads_dir / user_id / filename).resolve()
    if not str(requested_path).startswith(str(uploads_dir.resolve())):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not requested_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    media_type, _ = mimetypes.guess_type(str(requested_path))
    return FileResponse(str(requested_path), media_type=media_type or 'application/octet-stream')


@router.get('/{page_name}', response_class=HTMLResponse)
async def render_page(request: Request, page_name: str):
    """
    Render any HTML page from the templates directory by name.
    Example: /about will render about.html
    """
    return templates.TemplateResponse(f'{page_name}.html', {'request': request})
