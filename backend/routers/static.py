
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Mount static files (e.g., /static/style.css)
static_dir = os.path.join(os.path.dirname(__file__), '../static')
router.mount('/static', StaticFiles(directory=static_dir), name='static')

# Set up Jinja2 templates (e.g., /templates/index.html)
templates_dir = os.path.join(os.path.dirname(__file__), '../static/templates')
print(f"Templates directory: {templates_dir}")
templates = Jinja2Templates(directory=templates_dir)


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the home page (index.html) from the templates directory.
    """
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/{page_name}', response_class=HTMLResponse)
async def render_page(request: Request, page_name: str):
    """
    Render any HTML page from the templates directory by name.
    Example: /about will render about.html
    """
    return templates.TemplateResponse(f'{page_name}.html', {'request': request})
