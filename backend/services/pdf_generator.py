import os
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from jinja2 import Environment, FileSystemLoader
from fastapi import HTTPException
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Service for generating PDFs from HTML templates using Playwright Chrome engine"""

    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))

    async def generate_pdf(
        self,
        template_name: str,
        data: Dict[str, Any],
        output_format: str = "a4",
        orientation: str = "portrait",
        color_mode: str = "color",
        quality: str = "high",
        margin_top: str = "0.5in",
        margin_bottom: str = "0.5in",
        margin_left: str = "0.5in",
        margin_right: str = "0.5in"
    ) -> bytes:
        """
        Generate PDF from HTML template

        Args:
            template_name: Name of Jinja2 template
            data: Template data dictionary
            output_format: Paper format ('a4', 'letter', 'legal')
            orientation: Page orientation ('portrait', 'landscape')
            color_mode: Color mode ('color', 'black_and_white')
            quality: Print quality ('low', 'medium', 'high')
            margins: Page margins

        Returns:
            PDF bytes
        """
        async with async_playwright() as p:
            # Create browser context
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-gpu'
                ]
            )

            try:
                # Load and render template
                template = self.jinja_env.get_template(template_name)
                html_content = template.render(**data)

                # Create browser context and page
                context = await browser.new_context(
                    viewport={'width': 1200, 'height': 1600},
                    device_scale_factor=2 if quality == 'high' else 1
                )

                page = await context.new_page()

                # Set content and wait for it to load
                await page.set_content(html_content, wait_until='networkidle')

                # Wait for images to load
                await page.wait_for_function('''
                    () => {
                        const images = document.querySelectorAll('img');
                        return images.length === 0 || Array.from(images).every(img => img.complete);
                    }
                ''', timeout=10000)

                # Configure PDF options
                pdf_options = {
                    'format': output_format,
                    'landscape': orientation == 'landscape',
                    'print_background': color_mode == 'color',
                    'margin': {
                        'top': margin_top,
                        'bottom': margin_bottom,
                        'left': margin_left,
                        'right': margin_right
                    }
                }

                # Adjust quality settings
                if quality == 'high':
                    pdf_options['scale'] = 1.0
                elif quality == 'medium':
                    pdf_options['scale'] = 0.9
                else:  # low
                    pdf_options['scale'] = 0.8

                # Generate PDF
                pdf_bytes = await page.pdf(**pdf_options)

                await context.close()

                logger.info(
                    f"PDF generated successfully: {len(pdf_bytes)} bytes")
                return pdf_bytes

            except Exception as e:
                logger.error(f"PDF generation failed: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"PDF generation failed: {str(e)}"
                )
            finally:
                await browser.close()

    async def generate_flyer_pdf(
        self,
        pet_data: Dict[str, Any],
        **kwargs
    ) -> bytes:
        """
        Generate pet flyer PDF with default settings

        Args:
            pet_data: Pet and owner data
            **kwargs: Additional PDF generation options

        Returns:
            PDF bytes
        """
        return await self.generate_pdf(
            template_name="lost_pet_flyer.html",
            data=pet_data,
            output_format=kwargs.get('format', 'a4'),
            orientation=kwargs.get('orientation', 'portrait'),
            color_mode=kwargs.get('color_mode', 'color'),
            quality=kwargs.get('quality', 'high'),
            margin_top=kwargs.get('margin_top', '0.25in'),
            margin_bottom=kwargs.get('margin_bottom', '0.25in'),
            margin_left=kwargs.get('margin_left', '0.25in'),
            margin_right=kwargs.get('margin_right', '0.25in')
        )


# Singleton instance
_pdf_generator: Optional[PDFGenerator] = None


def get_pdf_generator() -> PDFGenerator:
    """Get or create PDF generator singleton"""
    global _pdf_generator

    if not _pdf_generator:
        # Get templates directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(
            current_dir, "..", "static", "flyers_templates"
        )

        _pdf_generator = PDFGenerator(templates_dir)

    return _pdf_generator
