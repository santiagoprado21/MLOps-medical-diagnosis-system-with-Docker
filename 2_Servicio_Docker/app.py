"""
Sistema de Diagnóstico Médico - Simulación de Modelo ML
Este servicio simula un modelo de Machine Learning para clasificación de enfermedades
"""

from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def modelo_diagnostico(temperatura, frecuencia_cardiaca, presion_arterial):
    """
    Función que simula un modelo de ML para diagnóstico médico.
    
    Parámetros:
        temperatura (float): Temperatura corporal en °C (normal: 36.5-37.5)
        frecuencia_cardiaca (int): Frecuencia cardíaca en bpm (normal: 60-100)
        presion_arterial (int): Presión arterial sistólica en mmHg (normal: 90-120)
    
    Retorna:
        str: Estado del diagnóstico (NO ENFERMO, ENFERMEDAD LEVE, 
             ENFERMEDAD AGUDA, ENFERMEDAD CRÓNICA, ENFERMEDAD TERMINAL)
    """
    
    # Conversión a tipos numéricos
    try:
        temp = float(temperatura)
        fc = int(frecuencia_cardiaca)
        pa = int(presion_arterial)
    except (ValueError, TypeError):
        return "ERROR: Valores inválidos"
    
    # Contadores de anomalías
    anomalias_leves = 0
    anomalias_moderadas = 0
    anomalias_graves = 0
    anomalias_criticas = 0
    
    # Análisis de temperatura
    if 37.5 < temp <= 38.0:
        anomalias_leves += 1
    elif 38.0 < temp <= 39.0:
        anomalias_moderadas += 1
    elif 39.0 < temp <= 40.5 or 33.0 <= temp < 35.0:
        anomalias_graves += 1
    elif temp > 40.5 or temp < 33.0:
        anomalias_criticas += 1
    
    # Análisis de frecuencia cardíaca
    if 100 < fc <= 110 or 50 <= fc < 60:
        anomalias_leves += 1
    elif 110 < fc <= 130 or 40 <= fc < 50:
        anomalias_moderadas += 1
    elif 130 < fc <= 150 or 30 <= fc < 40:
        anomalias_graves += 1
    elif fc > 150 or fc < 30:
        anomalias_criticas += 1
    
    # Análisis de presión arterial
    if (120 < pa <= 130) or (80 <= pa < 90):
        anomalias_leves += 1
    elif (130 < pa <= 160) or (70 <= pa < 80):
        anomalias_moderadas += 1
    elif (160 < pa <= 180) or (60 <= pa < 70):
        anomalias_graves += 1
    elif pa > 180 or pa < 60:
        anomalias_criticas += 1
    
    # Lógica de clasificación
    # Casos críticos/terminales: múltiples anomalías críticas o combinación extrema
    if anomalias_criticas >= 2 or (anomalias_criticas >= 1 and anomalias_graves >= 2):
        return "ENFERMEDAD TERMINAL"
    elif anomalias_criticas >= 1 or anomalias_graves >= 2:
        return "ENFERMEDAD AGUDA"
    elif anomalias_graves >= 1:
        return "ENFERMEDAD AGUDA"
    elif anomalias_moderadas >= 2:
        return "ENFERMEDAD CRÓNICA"
    elif anomalias_moderadas >= 1 or anomalias_leves >= 2:
        return "ENFERMEDAD LEVE"
    else:
        return "NO ENFERMO"


@app.route('/')
def home():
    """Página principal con formulario web"""
    return render_template('index.html')


@app.route('/predecir', methods=['POST'])
def predecir():
    """
    Endpoint para realizar predicciones.
    Acepta datos en formato JSON o form data.
    
    Ejemplo de request JSON:
    {
        "temperatura": 38.5,
        "frecuencia_cardiaca": 95,
        "presion_arterial": 130
    }
    """
    try:
        # Intentar obtener datos de JSON
        if request.is_json:
            data = request.get_json()
            temperatura = data.get('temperatura')
            frecuencia_cardiaca = data.get('frecuencia_cardiaca')
            presion_arterial = data.get('presion_arterial')
        else:
            # Obtener datos de formulario
            temperatura = request.form.get('temperatura')
            frecuencia_cardiaca = request.form.get('frecuencia_cardiaca')
            presion_arterial = request.form.get('presion_arterial')
        
        # Validar que todos los parámetros estén presentes
        if None in [temperatura, frecuencia_cardiaca, presion_arterial]:
            return jsonify({
                'error': 'Faltan parámetros requeridos',
                'parametros_requeridos': ['temperatura', 'frecuencia_cardiaca', 'presion_arterial']
            }), 400
        
        # Realizar predicción
        diagnostico = modelo_diagnostico(temperatura, frecuencia_cardiaca, presion_arterial)
        
        # Log de la predicción
        logger.info(f"Predicción realizada - Temp: {temperatura}, FC: {frecuencia_cardiaca}, "
                   f"PA: {presion_arterial} -> Resultado: {diagnostico}")
        
        # Retornar resultado
        return jsonify({
            'diagnostico': diagnostico,
            'parametros': {
                'temperatura': float(temperatura),
                'frecuencia_cardiaca': int(frecuencia_cardiaca),
                'presion_arterial': int(presion_arterial)
            }
        })
    
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({
        'status': 'healthy',
        'service': 'Sistema de Diagnóstico Médico',
        'version': '1.0.0'
    })


@app.route('/test', methods=['GET'])
def test_casos():
    """
    Endpoint para probar diferentes casos de diagnóstico
    """
    casos_prueba = [
        {
            'descripcion': 'Paciente saludable',
            'parametros': {'temperatura': 36.8, 'frecuencia_cardiaca': 75, 'presion_arterial': 110},
            'diagnostico': modelo_diagnostico(36.8, 75, 110)
        },
        {
            'descripcion': 'Enfermedad leve - Fiebre ligera',
            'parametros': {'temperatura': 37.8, 'frecuencia_cardiaca': 85, 'presion_arterial': 115},
            'diagnostico': modelo_diagnostico(37.8, 85, 115)
        },
        {
            'descripcion': 'Enfermedad aguda - Fiebre alta',
            'parametros': {'temperatura': 39.5, 'frecuencia_cardiaca': 110, 'presion_arterial': 140},
            'diagnostico': modelo_diagnostico(39.5, 110, 140)
        },
        {
            'descripcion': 'Enfermedad crónica - Hipertensión moderada',
            'parametros': {'temperatura': 37.0, 'frecuencia_cardiaca': 115, 'presion_arterial': 145},
            'diagnostico': modelo_diagnostico(37.0, 115, 145)
        },
        {
            'descripcion': 'Enfermedad terminal - Condiciones críticas múltiples',
            'parametros': {'temperatura': 41.5, 'frecuencia_cardiaca': 165, 'presion_arterial': 190},
            'diagnostico': modelo_diagnostico(41.5, 165, 190)
        }
    ]
    
    return jsonify({
        'casos_de_prueba': casos_prueba
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

