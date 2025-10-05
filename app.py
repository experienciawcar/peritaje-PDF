from flask import Flask, render_template, make_response, request, jsonify
#import pdfkit
from weasyprint import HTML

import os
# Mappers
from mappers import ActasMapper
import logging
import time


# === CONFIGURACIÓN DE LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger("pdf_worker")

# Reducir ruido de librerías internas
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)


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
    start_total = time.perf_counter()
    start_html = time.perf_counter()
    # Renderiza la plantilla usando Flask
    html = render_template("pagina_generada.html", is_pdf=True)
    end_html = time.perf_counter()
    print(f"Tiempo para renderizar HTML: {end_html - start_html:.2f} segundos")

    # Si usas recursos estáticos, define la base_url
    start_pdf = time.perf_counter()
    base_url = os.path.abspath(os.path.dirname(__file__))
    print("Voy a hacer el PDF", base_url)
    logger.info(f"Base URL for resources: {base_url}")
    # Genera el PDF desde el HTML renderizado
    pdf = HTML(string=html, base_url=base_url).write_pdf()
    end_pdf = time.perf_counter()
    print(f"Tiempo para generar PDF: {end_pdf - start_pdf:.2f} segundos")

    # Crear respuesta HTTP con el PDF
    start_response = time.perf_counter()
    response = make_response(pdf)
    end_response = time.perf_counter()
    print(f"Tiempo para crear respuesta HTTP: {end_response - start_response:.2f} segundos")
    logger.info("PDF response created for peritaje")
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=acta.pdf"
    print("hice response")
    logger.info("Response with PDF for peritaje created")


    return response



@app.post("/generate_actas")
def generate_actas_pdf():
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
