from flask import Flask, render_template, make_response, request, jsonify
import pdfkit
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de pdfkit con opciones adicionales
options = {
    'enable-local-file-access': None,
    'enable-smart-shrinking': None,
    'encoding': 'UTF-8',
    'print-media-type': None,
    'dpi': '300',
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'page-size': 'Letter',
    'quiet': '',

    # Ajustes de tamaño y escala
    'zoom': '1.5',
    'viewport-size': '1024x768',
    'page-width': '210mm',  # Ancho de página A4
    'page-height': '297mm', # Alto de página A4
    
    # Mejoras de renderizado
    'javascript-delay': '1000',
    'no-stop-slow-scripts': None,
    'zoom': '1.25',  # o '1.3' si quieres un pelín más grande
}

@app.route('/')
def index():
    data = {
            'numero_reporte': '0001',
            'client': {
                'name': 'Juan Perez',
                'address': 'Av. Siempre Viva 123',
                'document': '00.000.000',
                'phone': '1234567890',
                'email': 'juan.perez@example.com'
            },
            'vehicle': {
                'brand': 'Toyota',
                'model': 'Corolla',
                'year': '2020',
                'plate': 'ABC123',
                'color': 'Rojo',
                'kilometers': '1.000K',
                'body_type': 'Sedan',
                'transmission': 'Automático',
                'fuel_type': 'Gasolina',
                'engine_capacity': '1.5L',
                'horsepower': '120 HP',
                'version': 'LS',
                'register_owner': '1002347521',
            },
            'accident': {
                'accident_type': 'Perdida total por daños',
                'quantity': '0',
                'soat_date': '01 / 01 / 2025',
                'soat_number': '1234567890',
                'inspection_date': '01 / 01 / 2025',
            },
            'left_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte izquierda que requieren atención inmediata.'
            },
            'right_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.'
            },
            'back_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.'
            },
            'front_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.'
            },
            'roof_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.'
            },
            'floor_side': {
                'gravity_items': [
                    {'title': 'Golpe', 'gravity': '1'},
                    {'title': 'Rayones', 'gravity': '1'},
                    {'title': 'Choque', 'gravity': '4'},
                ],
                'image': 'https://storage.googleapis.com/course-gcp-2024-images/2025/04/30/472a74bc-b13b-4349-a47c-54d47d65086c.png',
                'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.',
                'items': [
                    {'title': 'Estructura de chasis', 'state': 'En buen estado', 'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.', 'price': '200,00 $'},
                    {'title': 'Punta de chasis', 'state': 'En buen estado', 'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.', 'price': '200,00 $'},
                    {'title': 'Piso general', 'state': 'En buen estado', 'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.', 'price': '200,00 $'},
                    {'title': 'Estribos', 'state': 'En buen estado', 'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.', 'price': '200,00 $'},
                    {'title': 'Traviesas', 'state': 'En buen estado', 'description': 'El vehículo presenta severos y preocupantes problemas en la parte derecha que requieren atención inmediata.', 'price': '200,00 $'},
                ]
            },
            'fecha': datetime.now().strftime('%d/%m/%Y'),
            'hora': datetime.now().strftime('%I:%M %p')
        }
    return render_template('report.html', **data)

@app.post('/generate_pdf')
def generate_pdf():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        # Validar que los datos requeridos estén presentes
        print(f"Saque los datos")
        if not data:
            print(f"No se proporcionaron datos: {data}")
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        print(f"Extrae los datos")
            
        # Extraer los datos necesarios del payload
        numero_reporte = data.get('numero_reporte')
        client = data.get('client', {})
        vehicle = data.get('vehicle', {})
        accident = data.get('accident', {})
        left_side = data.get('left_side', {})
        right_side = data.get('right_side', {})
        front_side = data.get('front_side', {})
        back_side = data.get('back_side', {})
        roof_side = data.get('roof_side', {})
        floor_side = data.get('floor_side', {})
        accessories = data.get('accessories',{})
        upholstery = data.get('upholstery',{})
        electrical_system = data.get('electrical_system',{})
        ventilation = data.get('ventilation',{})
        engine = data.get('engine',{})
        transmission = data.get('transmission',{})
        brakes = data.get('brakes',{})
        direction = data.get('direction',{})
        suspension = data.get('suspension',{})
        tires = data.get('tires',{})
        rin = data.get('rin',{})
        observations = data.get('observations',{})
        total_budget = data.get('total_budget',{})
        inspection_status = data.get('inspection_status',{})
        # Validar datos requeridos
        print(f"Validar datos requeridos")
        if not numero_reporte:
            print(f"No se proporcionó el número de reporte: {numero_reporte}")
            return jsonify({'error': 'El número de reporte es requerido'}), 400

        print(f"Renderiza la plantilla")
        # Renderizar la plantilla con los datos
        html = render_template('report.html',
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
                             inspection_status=inspection_status)
        
        print(f"HTML generado")
        
        # Convertir HTML a PDF con las opciones configuradas
        pdf = pdfkit.from_string(
            html,
            False,
            options=options
        )
        
        print(f"PDF generado")
        
        # Crear respuesta
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
        print(f"Respuesta creada")
        return response
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Puerto 8080 por defecto si no se define
    app.run(host='0.0.0.0', port=port)