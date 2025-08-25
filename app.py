from flask import Flask, render_template, make_response, request, jsonify
import pdfkit
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
    return render_template("actas.html")


@app.post("/generate_pdf")
def generate_pdf():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        # Validar que los datos requeridos estén presentes
        print(f"Saque los datos")
        if not data:
            print(f"No se proporcionaron datos: {data}")
            return jsonify({"error": "No se proporcionaron datos"}), 400

        # Extraer los datos necesarios del payload
        numero_reporte = data.get("numero_reporte")
        client = data.get("client", {})
        vehicle = data.get("vehicle", {})
        accident = data.get("accident", {})
        left_side = data.get("left_side", {})
        right_side = data.get("right_side", {})
        front_side = data.get("front_side", {})
        back_side = data.get("back_side", {})
        roof_side = data.get("roof_side", {})
        floor_side = data.get("floor_side", {})
        accessories = data.get("accessories", {})
        upholstery = data.get("upholstery", {})
        electrical_system = data.get("electrical_system", {})
        ventilation = data.get("ventilation", {})
        engine = data.get("engine", {})
        transmission = data.get("transmission", {})
        brakes = data.get("brakes", {})
        direction = data.get("direction", {})
        suspension = data.get("suspension", {})
        tires = data.get("tires", {})
        rin = data.get("rin", {})
        observations = data.get("observations", {})
        total_budget = data.get("total_budget", {})
        inspection_status = data.get("inspection_status", {})
        resumen = data.get("resumen", {})
        # Validar datos requeridos
        print(f"Validar datos requeridos")
        if not numero_reporte:
            print(f"No se proporcionó el número de reporte: {numero_reporte}")
            return jsonify({"error": "El número de reporte es requerido"}), 400

        print(f"Renderiza la plantilla")
        # Renderizar la plantilla con los datos
        html = render_template(
            "report.html",
            numero_reporte=numero_reporte,
            client=client,
            vehicle=vehicle,
            accident=accident,
            left_side=left_side,
            right_side=right_side,
            front_side=front_side,
            back_side=back_side,
            roof_side=roof_side,
            floor_side=floor_side,
            accessories=accessories,
            upholstery=upholstery,
            electrical_system=electrical_system,
            ventilation=ventilation,
            engine=engine,
            transmission=transmission,
            brakes=brakes,
            direction=direction,
            suspension=suspension,
            tires=tires,
            rin=rin,
            observations=observations,
            total_budget=total_budget,
            inspection_status=inspection_status,
            resumen=resumen,
        )

        print(f"HTML generado")

        # Convertir HTML a PDF con las opciones configuradas
        pdf = pdfkit.from_string(html, False, options=options)

        print(f"PDF generado")

        # Crear respuesta
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=report.pdf"
        print(f"Respuesta creada")
        return response
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        return str(e), 500


@app.route("/generate_pdf_test", methods=["GET"])
def generate_pdf_test():
    print("Accessing generate_pdf_test endpoint")
    try:
        # Datos hardcodeados para pruebas
        data = {
            "client": {
                "name": "Pruebas pruebas",
                "document": "00011133",
                "phone": "3175489822",
                "address": "Calebshsj",
                "email": "sebastian.msp86@gmail.com",
            },
            "numero_reporte": 1293,
            "vehicle": {
                "brand": "BAJAJ",
                "model": "",
                "year": 2016,
                "color": "NEGRO NEBULOSA",
                "plate": "GZK936",
                "kilometers": "86074",
                "body_type": "SIN CARROCERIA",
                "transmission": 1,
                "engine": "",
                "fuel_type": "Gasolina",
                "register_owner": "51942457",
                "version": "PULSAR 135 LS",
            },
            "accident": {
                "siniestro": "",
                "compliance": False,
                "quantity": "100000000",
                "soat_date": "26/11/2024",
                "vehicle_inspection_date": "12/12/2024",
            },
            "resumen": {
                "budgets": {
                    "vehicle_exterior": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "100",
                    },
                    "vehicle_interior": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "90",
                    },
                    "vehicle_underbody": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "80",
                    },
                    "ventilation": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "70",
                    },
                    "engine": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "60",
                    },
                    "transmision": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "50",
                    },
                    "brakes": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "40",
                    },
                    "direction": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "30",
                    },
                    "suspension": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "20",
                    },
                    "tires": {
                        "budget_suggested": "$ 180.000",
                        "budget_percentage": "10",
                    },
                    "total_budget": "$ 1.800.000",
                },
                "observations": {
                    "general_observations": "El vehículo presenta un estado general regular, con algunos problemas menores en la carrocería y el sistema de suspensión. Se recomienda realizar las reparaciones sugeridas para mejorar su funcionamiento y seguridad.",
                    "price_observations": "El precio sugerido para las reparaciones es de $1.800.000, lo cual es razonable considerando el estado del vehículo y las reparaciones necesarias.",
                    "price_suggested": "$ 120.800.000",
                },
                "vehicle": {
                    "brand": "BAJAJ",
                    "model": "",
                    "year": 2016,
                    "reference": "PULSAR 135 LS",
                    "plate": "GZK936",
                    "kilometers": "86074",
                    "bodywork": "Sedan",
                    "transmission": "Manual",
                    "color": "NEGRO NEBULOSA",
                },
                "vehicle_compliance": {
                    "is_compliant": False,
                    "reason": "El vehículo no cumple con los estándares de seguridad y funcionamiento requeridos debido a las fallas detectadas en el sistema de suspensión y frenos.",
                    "type": "Perdida total",
                },
            },
            "accessories": {
                "parlantes": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "alarma": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "exploradoras": {
                    "state": "Malo",
                    "description": "fundidas",
                    "price": "$500,000.00 COP",
                },
                "aire_acondicionado": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "bloqueo_central": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "luces_generales": {
                    "state": "En estado regular",
                    "description": "funcionan",
                    "price": "N/A",
                },
                "pelicula_de_seguridad": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "seguros": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "tapiceria_en_cuero": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "total_price": "$500,000.00",
                "observations": "Se observa que el vehículo presenta algunas fallas en los accesorios, principalmente en las exploradoras que se encuentran fundidas y requieren reemplazo. Las luces generales funcionan pero se recomienda darles mantenimiento preventivo. El resto de los accesorios se encuentran en buen estado de funcionamiento.",
            },
            "upholstery": {
                "limpieza_tapiceria": {
                    "state": "En estado regular",
                    "description": "manchas por sol",
                    "price": "$250,000.00 COP",
                },
                "estado_tapiceria": {
                    "state": "En buen estado",
                    "description": "bueno",
                    "price": "N/A",
                },
                "ajuste_de_sillas": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "cinturon_de_seguridad": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "estado_de_millare": {
                    "state": "En estado regular",
                    "description": "desgastado",
                    "price": "$480,000.00 COP",
                },
                "alfombra": {
                    "state": "Malo",
                    "description": "desgastado",
                    "price": "$275,300.00 COP",
                },
                "tapetes": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "manijas_interiores": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "timon": {
                    "state": "En estado regular",
                    "description": "desgaste por el sol",
                    "price": "$100,000.00 COP",
                },
                "otros_defectos": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$1,105,300.00",
                "observations": "",
            },
            "electrical_system": {
                "radio": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "N/A",
                },
                "testigos_tablero": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "N/A",
                },
                "luces_de_emergencia": {
                    "state": "En estado regular",
                    "description": "fundidas",
                    "price": "$50,000.00 COP",
                },
                "limpia_parabrisas": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "reloj": {"state": "En buen estado", "description": "", "price": "N/A"},
                "velocimetro": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "tacometro": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "alternador": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "bateria": {
                    "state": "En estado regular",
                    "description": "media capacidad",
                    "price": "$500,000.00 COP",
                },
                "luces_generales": {
                    "state": "En estado regular",
                    "description": "funcionan",
                    "price": "N/A",
                },
                "otros": {"state": "N/A", "description": "N/A", "price": "N/A"},
                "total_price": "$550,000.00",
                "observations": "",
            },
            "ventilation": {
                "aire_acondicionado": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "electro_ventilacion_aa": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "rejillas_ventilacion": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "N/A",
                },
                "calefaccion": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "controles_de_mando": {
                    "state": "Muy malo",
                    "description": "no funcionan",
                    "price": "$250,000.00 COP",
                },
                "motor_de_calefaccion": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "tuberia_aire": {
                    "state": "En estado regular",
                    "description": "okj",
                    "price": "N/A",
                },
                "ruidos_anormales": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "total_price": "$250,000.00 COP",
                "observations": "bduejdjd",
            },
            "engine": {
                "nivel_del_refrigerante": {
                    "state": "En estado regular",
                    "description": "mexio6",
                    "price": "N/A",
                },
                "operacion_motor": {
                    "state": "En estado regular",
                    "description": "bueno",
                    "price": "$100,000.00 COP",
                },
                "fugas_de_aceite": {
                    "state": "Malo",
                    "description": "fugas en mangeras",
                    "price": "$480,000.00 COP",
                },
                "compresion": {
                    "state": "En estado regular",
                    "description": "buena comprensión",
                    "price": "$65,000.00 COP",
                },
                "lados": {
                    "state": "En estado regular",
                    "description": "7g7t7gugj",
                    "price": "$25,000.00 COP",
                },
                "lodos": {"state": "N/A", "description": "N/A", "price": "N/A"},
                "soportes": {
                    "state": "Muy malo",
                    "description": "kgigug679",
                    "price": "$698,000.00 COP",
                },
                "filtro_de_aire": {
                    "state": "En estado regular",
                    "description": "bdhdjs",
                    "price": "$100,000.00 COP",
                },
                "filtro_de_aceite": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "correa_de_reparticion": {
                    "state": "En estado regular",
                    "description": "hdjdbd",
                    "price": "$100,000.00 COP",
                },
                "correa_accesorios": {
                    "state": "Malo",
                    "description": "bxjsjsmxbc",
                    "price": "$67,000.00 COP",
                },
                "ruidos_anormales": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "retenedores": {
                    "state": "En buen estado",
                    "description": "j1jd un djg",
                    "price": "N/A",
                },
                "total_price": "$1,635,000.00 COP",
                "observations": "",
            },
            "transmission": {
                "transmision": {
                    "state": "En estado regular",
                    "description": "jzuskd",
                    "price": "$200,000.00 COP",
                },
                "golpeteo_en_caja": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "ruidos_anormales": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "dificultad_de_cambios": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "cambios_bruscos": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "fugas_de_aceite": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "traccion_en_ruedas": {
                    "state": "En estado regular",
                    "description": "vxjsjsnaoow",
                    "price": "$100,000.00 COP",
                },
                "embrague": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "nivel_de_aceite": {
                    "state": "Malo",
                    "description": "bajo",
                    "price": "$45,000.00 COP",
                },
                "otros_defectos": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$345,000.00 COP",
                "observations": "",
            },
            "brakes": {
                "nivel_de_fluidos": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "N/A",
                },
                "ruidos_anormales": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "testigo_ruido_al_frenar": {
                    "state": "Malo",
                    "description": "cambio pastillas",
                    "price": "$700,000.00 COP",
                },
                "vibracion_al_frenar": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "freno_de_mano": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "fugas_de_liquido": {
                    "state": "En estado regular",
                    "description": "hzjsbd",
                    "price": "$200,000.00 COP",
                },
                "disco_izquierdo_frontal": {
                    "state": "Malo",
                    "description": "ndjsjdnd",
                    "price": "$200,000.00 COP",
                },
                "disco_derecho_frontal": {
                    "state": "Malo",
                    "description": "jzjsjs d",
                    "price": "$100,000.00 COP",
                },
                "disco_izquierdo_trasero": {
                    "state": "En estado regular",
                    "description": "ok",
                    "price": "N/A",
                },
                "disco_derecho_trasero": {
                    "state": "En estado regular",
                    "description": "guiv",
                    "price": "$100,000.00 COP",
                },
                "retenedores": {
                    "state": "En estado regular",
                    "description": "zjjs",
                    "price": "$300,000.00 COP",
                },
                "otros_defectos": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$1,600,000.00 COP",
                "observations": "",
            },
            "direction": {
                "estado_direccion": {
                    "state": "En estado regular",
                    "description": "jdudkdn",
                    "price": "$100,000.00 COP",
                },
                "nivel_de_aceite": {
                    "state": "Malo",
                    "description": "kdusjdn",
                    "price": "$200,000.00 COP",
                },
                "estado_del_aceite": {
                    "state": "En buen estado",
                    "description": "gggxv",
                    "price": "$100,000.00 COP",
                },
                "fugas_aceite": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "desempeno_direccion": {
                    "state": "En estado regular",
                    "description": "jzjdjd",
                    "price": "$500,000.00 COP",
                },
                "terminales": {
                    "state": "En estado regular",
                    "description": "bdjsol",
                    "price": "$100,000.00 COP",
                },
                "alineacion_direccion": {
                    "state": "En estado regular",
                    "description": "jxusnd",
                    "price": "$100,000.00 COP",
                },
                "orientacion_timon": {
                    "state": "En estado regular",
                    "description": "ktcv",
                    "price": "$200,000.00 COP",
                },
                "otros_problemas": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$1,300,000.00 COP",
                "observations": "",
            },
            "suspension": {
                "guarda_polvos": {
                    "state": "En estado regular",
                    "description": "suheksmd",
                    "price": "$300,000.00 COP",
                },
                "retenes": {
                    "state": "En estado regular",
                    "description": "jxjskdbx",
                    "price": "$200,000.00 COP",
                },
                "amortiguador_delantero_izquierdo": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "N/A",
                },
                "amortiguador_delantero_derecho": {
                    "state": "En estado regular",
                    "description": "keuejd",
                    "price": "$200,000.00 COP",
                },
                "amortiguador_trasero_izquierdo": {
                    "state": "En estado regular",
                    "description": "9k",
                    "price": "$200,000.00 COP",
                },
                "amortiguador_trasero_derecho": {
                    "state": "En estado regular",
                    "description": "ususbbe",
                    "price": "$100,000.00 COP",
                },
                "brazos_suspension": {
                    "state": "En buen estado",
                    "description": "ok",
                    "price": "$200,000.00 COP",
                },
                "bujes_o_cauchos": {
                    "state": "Malo",
                    "description": "ksksksndnd",
                    "price": "$100,000.00 COP",
                },
                "rodamiento_delantero_izquierdo": {
                    "state": "En estado regular",
                    "description": "jxisnd",
                    "price": "$2,500,000.00 COP",
                },
                "rodamiento_delantero_derecho": {
                    "state": "En estado regular",
                    "description": "jdjdk",
                    "price": "$100,000.00 COP",
                },
                "rodamiento_trasero_izquierdo": {
                    "state": "En estado regular",
                    "description": "jzjskdnxkclvk",
                    "price": "$223,000.00 COP",
                },
                "rodamiento_trasero_derecho": {
                    "state": "Muy malo",
                    "description": "xjjdjx",
                    "price": "$326,000.00 COP",
                },
                "otros_defectos": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$4,449,000.00 COP",
                "observations": "",
            },
            "tires": {
                "llantas_delanteras": {
                    "state": "En estado regular",
                    "description": "jgfh",
                    "price": "$100,000.00 COP",
                },
                "llantas_traseras": {
                    "state": "Muy malo",
                    "description": "jhffdd",
                    "price": "$800,000.00 COP",
                },
                "llanta_de_repuesto": {
                    "state": "En buen estado",
                    "description": "",
                    "price": "N/A",
                },
                "total_price": "$1,200,000.00 COP",
                "observations": "",
            },
            "rin": {
                "rines_delanteros": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "rines_traseros": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "rin_trasero_izquierdo": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "rin_trasero_derecho": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "rin_de_repuesto": {
                    "state": "N/A",
                    "description": "N/A",
                    "price": "N/A",
                },
                "total_price": "$0.00 COP",
                "observations": "",
            },
            "total_budget": "$26,000,000.00 COP",
            "observations": "Después de una inspección exhaustiva del vehículo, se puede concluir que es una excelente opción de compra. El estado general del motor es satisfactorio, con solo algunas reparaciones menores necesarias. La carrocería presenta daños menores que pueden ser reparados sin mayor complicación. El sistema de transmisión funciona correctamente y los sistemas eléctricos están en buen estado. El vehículo ha sido bien mantenido y su kilometraje es consistente con su edad. Se recomienda proceder con la compra, ya que el precio solicitado es razonable considerando el estado general del vehículo y los costos estimados de reparación.",
            "left_side": {
                "image": "https://storage.googleapis.com/wcar-images/cars-43715702-1IMG_6530.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=githubactions%40web-wcar-co.iam.gserviceaccount.com%2F20250514%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250514T035926Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=33141619bc537014c409efcd09f50473e113b0dd5d54bdd8633d670ac61af60fe950582cb17d989d9601280cde06682d7a14c86239a24ebc5d8d2c764bc010a1247c7e5a67c982e12b868f110bc95e89a2cbfecf31054b1384010b0568ee4e57a0522e2cedc6b147a0c963a91cb04f9647f53c7bc54dde9115e788c7719c92bc32c9bc46c345ddb7636b3d5d0ed79080284760c09c88cd55ff6aa204837fa47c79d6fd148c910e6e2180f67973e8f4bc08d2190956454f91bbd41fe8ee6df23e0f4da69d38ad795f77a52bfef9e617fb23a53ee47a801747f6c77f4213deb02d7f2dde6ed0264437a20c6b8b4b0f385e088e49e42245356de87088bc57b7e0f6",
                "gravity_items": [],
                "description": "latonería dhsksjdj",
                "budget": "$300,000.00 COP",
            },
            "back_side": {
                "image": "https://storage.googleapis.com/wcar-images/cars-43715702-1IMG_6530.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=githubactions%40web-wcar-co.iam.gserviceaccount.com%2F20250514%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250514T035926Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=33141619bc537014c409efcd09f50473e113b0dd5d54bdd8633d670ac61af60fe950582cb17d989d9601280cde06682d7a14c86239a24ebc5d8d2c764bc010a1247c7e5a67c982e12b868f110bc95e89a2cbfecf31054b1384010b0568ee4e57a0522e2cedc6b147a0c963a91cb04f9647f53c7bc54dde9115e788c7719c92bc32c9bc46c345ddb7636b3d5d0ed79080284760c09c88cd55ff6aa204837fa47c79d6fd148c910e6e2180f67973e8f4bc08d2190956454f91bbd41fe8ee6df23e0f4da69d38ad795f77a52bfef9e617fb23a53ee47a801747f6c77f4213deb02d7f2dde6ed0264437a20c6b8b4b0f385e088e49e42245356de87088bc57b7e0f6",
                "gravity_items": [],
                "description": "ok",
                "budget": "N/A",
            },
            "right_side": {
                "image": "https://storage.googleapis.com/wcar-images/cars-43715702-1IMG_6530.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=githubactions%40web-wcar-co.iam.gserviceaccount.com%2F20250514%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250514T035926Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=33141619bc537014c409efcd09f50473e113b0dd5d54bdd8633d670ac61af60fe950582cb17d989d9601280cde06682d7a14c86239a24ebc5d8d2c764bc010a1247c7e5a67c982e12b868f110bc95e89a2cbfecf31054b1384010b0568ee4e57a0522e2cedc6b147a0c963a91cb04f9647f53c7bc54dde9115e788c7719c92bc32c9bc46c345ddb7636b3d5d0ed79080284760c09c88cd55ff6aa204837fa47c79d6fd148c910e6e2180f67973e8f4bc08d2190956454f91bbd41fe8ee6df23e0f4da69d38ad795f77a52bfef9e617fb23a53ee47a801747f6c77f4213deb02d7f2dde6ed0264437a20c6b8b4b0f385e088e49e42245356de87088bc57b7e0f6",
                "gravity_items": [],
                "description": "en puerta y trasera",
                "budget": "$550,000.00 COP",
            },
            "roof_side": {
                "image": "https://storage.googleapis.com/wcar-images/cars-43715702-1IMG_6530.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=githubactions%40web-wcar-co.iam.gserviceaccount.com%2F20250514%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250514T035926Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=33141619bc537014c409efcd09f50473e113b0dd5d54bdd8633d670ac61af60fe950582cb17d989d9601280cde06682d7a14c86239a24ebc5d8d2c764bc010a1247c7e5a67c982e12b868f110bc95e89a2cbfecf31054b1384010b0568ee4e57a0522e2cedc6b147a0c963a91cb04f9647f53c7bc54dde9115e788c7719c92bc32c9bc46c345ddb7636b3d5d0ed79080284760c09c88cd55ff6aa204837fa47c79d6fd148c910e6e2180f67973e8f4bc08d2190956454f91bbd41fe8ee6df23e0f4da69d38ad795f77a52bfef9e617fb23a53ee47a801747f6c77f4213deb02d7f2dde6ed0264437a20c6b8b4b0f385e088e49e42245356de87088bc57b7e0f6",
                "gravity_items": [],
                "description": "ok",
                "budget": "N/A",
            },
            "front_side": {
                "image": "https://storage.googleapis.com/wcar-images/cars-43715702-1IMG_6530.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=githubactions%40web-wcar-co.iam.gserviceaccount.com%2F20250514%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250514T035926Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=33141619bc537014c409efcd09f50473e113b0dd5d54bdd8633d670ac61af60fe950582cb17d989d9601280cde06682d7a14c86239a24ebc5d8d2c764bc010a1247c7e5a67c982e12b868f110bc95e89a2cbfecf31054b1384010b0568ee4e57a0522e2cedc6b147a0c963a91cb04f9647f53c7bc54dde9115e788c7719c92bc32c9bc46c345ddb7636b3d5d0ed79080284760c09c88cd55ff6aa204837fa47c79d6fd148c910e6e2180f67973e8f4bc08d2190956454f91bbd41fe8ee6df23e0f4da69d38ad795f77a52bfef9e617fb23a53ee47a801747f6c77f4213deb02d7f2dde6ed0264437a20c6b8b4b0f385e088e49e42245356de87088bc57b7e0f6",
                "gravity_items": [],
                "description": "corrosión",
                "budget": "$200,000.00 COP",
            },
            "floor_side": {
                "items": [
                    {
                        "title": "Estructura Chasis",
                        "state": "En buen estado",
                        "description": "hdjsjdbd",
                        "budget": 600000.0,
                    },
                    {
                        "title": "Punta Chasis",
                        "state": "En buen estado",
                        "description": "hdhsjs",
                        "budget": 100000.0,
                    },
                    {
                        "title": "Pisos General",
                        "state": "En buen estado",
                        "description": "ok",
                        "budget": 0.0,
                    },
                    {
                        "title": "Estribos",
                        "state": "En buen estado",
                        "description": "hdjsjdbw",
                        "budget": 200000.0,
                    },
                    {
                        "title": "Traviesas",
                        "state": "En buen estado",
                        "description": "hdudjw",
                        "budget": 100000.0,
                    },
                ]
            },
            "inspection_status": {
                "status": "Aceptado",
                "perito": "Usuario de Test Inspector",
                "commercial_advisor": "Luis Jose Torres",
            },
        }

        # Renderizar la plantilla con los datos
        html = render_template("report.html", **data)

        # Convertir HTML a PDF con las opciones configuradas
        pdf = pdfkit.from_string(html, False, options=options)

        # Crear respuesta
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=report.pdf"

        return response
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        return str(e), 500

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
    app.run(host="0.0.0.0", port=port)
