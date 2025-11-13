"""
Sistema de Diagnóstico Médico - Simulación de Modelo ML
Este servicio simula un modelo de Machine Learning para clasificación de enfermedades
"""

from flask import Flask, request, jsonify, render_template
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Archivo para almacenar predicciones
PREDICTIONS_FILE = 'predictions_log.json'


def guardar_prediccion(temperatura, frecuencia_cardiaca, presion_arterial, diagnostico):
    """
    Guarda una predicción en el archivo de registro.
    """
    prediccion = {
        'timestamp': datetime.now().isoformat(),
        'parametros': {
            'temperatura': float(temperatura),
            'frecuencia_cardiaca': int(frecuencia_cardiaca),
            'presion_arterial': int(presion_arterial)
        },
        'diagnostico': diagnostico
    }
    
    # Leer predicciones existentes
    predicciones = []
    if os.path.exists(PREDICTIONS_FILE):
        try:
            with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
                predicciones = json.load(f)
        except (json.JSONDecodeError, IOError):
            predicciones = []
    
    # Agregar nueva predicción
    predicciones.append(prediccion)
    
    # Guardar todas las predicciones
    try:
        with open(PREDICTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(predicciones, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f"Error al guardar predicción: {str(e)}")


def leer_predicciones():
    """
    Lee todas las predicciones del archivo de registro.
    """
    if not os.path.exists(PREDICTIONS_FILE):
        return []
    
    try:
        with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error al leer predicciones: {str(e)}")
        return []


def modelo_diagnostico(temperatura, frecuencia_cardiaca, presion_arterial):
    """
    Función que simula un modelo de ML para diagnóstico médico.
    
    Parámetros:
        temperatura (float): Temperatura corporal en °C (normal: 36.5-37.5)
        frecuencia_cardiaca (int): Frecuencia cardíaca en bpm (normal: 60-100)
        presion_arterial (int): Presión arterial sistólica en mmHg (normal: 90-120)
    
    Retorna:
        str: Estado del diagnóstico (NO ENFERMO, ENFERMEDAD LEVE, 
             ENFERMEDAD AGUDA, ENFERMEDAD CRÓNICA)
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
    
    # Análisis de temperatura
    if 37.5 < temp <= 38.0:
        anomalias_leves += 1
    elif 38.0 < temp <= 39.0:
        anomalias_moderadas += 1
    elif temp > 39.0 or temp < 35.0:
        anomalias_graves += 1
    
    # Análisis de frecuencia cardíaca
    if 100 < fc <= 110 or 50 <= fc < 60:
        anomalias_leves += 1
    elif 110 < fc <= 130 or 40 <= fc < 50:
        anomalias_moderadas += 1
    elif fc > 130 or fc < 40:
        anomalias_graves += 1
    
    # Análisis de presión arterial
    if (120 < pa <= 130) or (80 <= pa < 90):
        anomalias_leves += 1
    elif (130 < pa <= 160) or (70 <= pa < 80):
        anomalias_moderadas += 1
    elif pa > 160 or pa < 70:
        anomalias_graves += 1
    
    # Lógica de clasificación
    if anomalias_graves >= 1:
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
        
        # Guardar predicción en archivo
        guardar_prediccion(temperatura, frecuencia_cardiaca, presion_arterial, diagnostico)
        
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


@app.route('/reporte', methods=['GET'])
def generar_reporte():
    """
    Endpoint para obtener estadísticas de las predicciones realizadas.
    
    Retorna:
        - Número total de predicciones por categoría
        - Últimas 5 predicciones realizadas
        - Fecha de la última predicción
    """
    predicciones = leer_predicciones()
    
    if not predicciones:
        return jsonify({
            'mensaje': 'No hay predicciones registradas',
            'total_predicciones': 0,
            'predicciones_por_categoria': {},
            'ultimas_5_predicciones': [],
            'fecha_ultima_prediccion': None
        })
    
    # Contar predicciones por categoría
    predicciones_por_categoria = {}
    for pred in predicciones:
        diagnostico = pred['diagnostico']
        predicciones_por_categoria[diagnostico] = predicciones_por_categoria.get(diagnostico, 0) + 1
    
    # Obtener últimas 5 predicciones
    ultimas_5 = predicciones[-5:] if len(predicciones) >= 5 else predicciones
    ultimas_5.reverse()  # Mostrar la más reciente primero
    
    # Obtener fecha de última predicción
    fecha_ultima = predicciones[-1]['timestamp']
    
    return jsonify({
        'total_predicciones': len(predicciones),
        'predicciones_por_categoria': predicciones_por_categoria,
        'ultimas_5_predicciones': ultimas_5,
        'fecha_ultima_prediccion': fecha_ultima,
        'resumen': {
            'total': len(predicciones),
            'categorias': list(predicciones_por_categoria.keys()),
            'ultima_actualizacion': fecha_ultima
        }
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
        }
    ]
    
    return jsonify({
        'casos_de_prueba': casos_prueba
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

