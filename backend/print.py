from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime


def generar_pdf():
    # Configurar Jinja2
    env = Environment(loader=FileSystemLoader(
        '/home/pablushka/projects/petto/apps/frontend/static/flyers_templates/'))
    template = env.get_template(
        'lost_pet_flyer.html')

    # Datos de ejemplo
    datos = {
        "pet_name": "Rexy29",
        "pet_type": "Dog",
        "pet_age": "",
        "pet_breed": "",
        "pet_color": "",
        "pet_gender": "",
        "pet_last_seen": "",
        "pet_location": "",
        "pet_description": "Perrito pekin\u00e9s muy mal humorado. Muerde si tiene miedo, pero es f\u00e1cil de capturar si lo tomas por la nuca. Le gustan mucho el sushi, es una buena forma de capturarlo.",
        "pet_picture": "http://localhost:8000/static/uploads/1/b81e70d3ef63482b838920caf015b33a.jpg",
        "pet_picture2": "http://localhost:8000/static/uploads/1/c741023e19bc49a08b49fe23e4a423fe.jpg",
        "pet_picture3": "http://localhost:8000/static/uploads/1/354769eb1cfe414f90ec10c673e748a6.png",
        "pet_picture4": "http://localhost:8000/static/uploads/1/4eab40e9649d479f9d45556d73adef31.jpg",
        "pet_picture5": "http://localhost:8000/static/uploads/1/0a8cb5e381f541f3a69a67958147f4a1.png",
        "qr_code_url": "http://localhost:8000/api/qrcode/1",
        "owner_name": "Pablo Centurion",
        "owner_phone": "1150134235",
        "owner_email": "pablo@nomades.com.ar",
        "owner_address": "Liniers 1825",
        "reward_amount": "",
        "show_reward": False,
        "print_mode": "color",
        "pet_id": 1
    }

    # Renderizar template con datos
    html_content = template.render(**datos)

    print(html_content)

    # Generar PDF
    HTML(string=html_content).write_pdf('factura_ejemplo.pdf')

    print("PDF generado exitosamente: factura_ejemplo.pdf")


if __name__ == "__main__":
    generar_pdf()
