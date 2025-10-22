from flask import Flask, render_template, make_response, request, jsonify
#import pdfkit
from weasyprint import HTML

import os
# Mappers
from mappers import ActasMapper

app = Flask(__name__)
print("Flask app initialized")


@app.route("/test")
def test():
    return "Server is running!"


# Configuración de pdfkit con opciones adicionales
options = {
    "enable-local-file-access": None,
    "enable-smart-shrinking": None,
    "encoding": "UTF-8",
    "print-media-type": None,
    "dpi": "300",
    "margin-top": "0",
    "margin-right": "0",
    "margin-bottom": "0",
    "margin-left": "0",
    "page-size": "Letter",
    "quiet": "",
    # Ajustes de tamaño y escala
    "zoom": "1.5",
    "viewport-size": "1024x768",
    "page-width": "210mm",  # Ancho de página A4
    "page-height": "297mm",  # Alto de página A4
    # Mejoras de renderizado
    "javascript-delay": "1000",
    "no-stop-slow-scripts": None,
    "zoom": "1.25",  # o '1.3' si quieres un pelín más grande
}


@app.route("/")
def index():
    return render_template("pagina_generada.html", is_pdf=False)

@app.route("/generate_peritaje", methods=["GET"])
def generate_peritaje():
    print("Accessing generate_pdf endpoint")
    # Renderiza la plantilla usando Flask
    html = render_template("pagina_generada.html", is_pdf=True)
    print("hice html")

    # Si usas recursos estáticos, define la base_url
    base_url = os.path.abspath(os.path.dirname(__file__))
    print("Voy a hacer el PDF", base_url)
    # Genera el PDF desde el HTML renderizado
    pdf = HTML(string=html, base_url=base_url).write_pdf()
    print("hice pdf")

    # Crear respuesta HTTP con el PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=acta.pdf"
    print("hice response")

    return response



@app.route("/actas")
def actas_html():
    """Visualizar el HTML del acta con datos de ejemplo"""
    sample_data = {
        "id": 12345,
        "operation_date": "2025-10-22",
        "operation_hour": "10:30",
        "operation_type": 1,
        "observations": "El vehículo presenta un rayón menor en el guardabarros delantero derecho.",
        "gasoil_level": "acceptable",
        "client": {
            "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            "full_name": "Ana María Pérez",
            "document_number": "1030456789",
            "email": "ana.perez@example.com",
            "address": "Calle 10 # 5-20, Bogotá",
            "phone_number": "3101234567"
        },
        "vehicle": {
            "plate": "ABC123",
            "year": 2022,
            "brand": "Toyota",
            "reference": "Corolla Cross",
            "color": "Gris Metálico",
            "mileage": 15500,
            "soat_date": "2026-03-01",
            "rtm_date": "2026-03-01",
            "body_work": "En buen estado general, con un detalle en pintura."
        },
        "inventary": {
            "soat": True,
            "property_card": True,
            "rtm": True,
            "rugs": True,
            "compressor": False,
            "radio": True,
            "taxes": True,
            "folders": False,
            "manuals": True,
            "lug_wrench_crossbar": True,
            "jack": True,
            "lug_wrench": True,
            "road_kit": True,
            "key_duplicate": False,
            "spare_tire": True
        },
        "user": {
            "full_name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@wcar.com",
            "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        }
    }

    mapper = ActasMapper(sample_data).map()
    return render_template("actas.html", **mapper)


@app.route("/generate_actas", methods=["GET"])
def generate_actas_pdf_get():
    """Generar PDF del acta con datos de ejemplo (GET)"""
    sample_data = {
        "id": 12345,
        "operation_date": "2025-10-22",
        "operation_hour": "10:30",
        "operation_type": 1,
        "observations": "El vehículo presenta un rayón menor en el guardabarros delantero derecho.",
        "gasoil_level": "acceptable",
        "client": {
            "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            "full_name": "Ana María Pérez",
            "document_number": "1030456789",
            "email": "ana.perez@example.com",
            "address": "Calle 10 # 5-20, Bogotá",
            "phone_number": "3101234567"
        },
        "vehicle": {
            "plate": "ABC123",
            "year": 2022,
            "brand": "Toyota",
            "reference": "Corolla Cross",
            "color": "Gris Metálico",
            "mileage": 15500,
            "soat_date": "2026-03-01",
            "rtm_date": "2026-03-01",
            "body_work": "En buen estado general, con un detalle en pintura."
        },
        "inventary": {
            "soat": True,
            "property_card": True,
            "rtm": True,
            "rugs": True,
            "compressor": False,
            "radio": True,
            "taxes": True,
            "folders": False,
            "manuals": True,
            "lug_wrench_crossbar": True,
            "jack": True,
            "lug_wrench": True,
            "road_kit": True,
            "key_duplicate": False,
            "spare_tire": True
        },
        "user": {
            "full_name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@wcar.com",
            "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        }
    }

    mapper = ActasMapper(sample_data).map()

    # Renderiza la plantilla usando Flask
    html = render_template("actas.html", **mapper)

    # Si usas recursos estáticos, define la base_url
    base_url = os.path.abspath(os.path.dirname(__file__))

    # Genera el PDF desde el HTML renderizado
    pdf = HTML(string=html, base_url=base_url).write_pdf()
    print("PDF del acta generado")

    # Crear respuesta HTTP con el PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=acta.pdf"

    return response


@app.post("/generate_actas")
def generate_actas_pdf():
    """Generar PDF del acta con datos del request (POST)"""
    payload = request.get_json()
    mapper = ActasMapper(payload).map()

    # Renderiza la plantilla usando Flask
    html = render_template("actas.html", **mapper)

    # Si usas recursos estáticos, define la base_url
    base_url = os.path.abspath(os.path.dirname(__file__))

    # Genera el PDF desde el HTML renderizado
    pdf = HTML(string=html, base_url=base_url).write_pdf()
    print("hice pdf")

    # Crear respuesta HTTP con el PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=acta.pdf"
    print("hice response")

    return response



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Puerto 8080 por defecto si no se define
    app.run(host="0.0.0.0", port=port, debug=True)
