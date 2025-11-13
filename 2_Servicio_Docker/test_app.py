"""
Pruebas unitarias para el Sistema de Diagnóstico Médico
"""

import pytest
import json
import os
from app import app, modelo_diagnostico, PREDICTIONS_FILE


@pytest.fixture
def client():
    """Fixture para cliente de pruebas de Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def limpiar_predicciones():
    """Fixture para limpiar el archivo de predicciones antes de cada prueba"""
    if os.path.exists(PREDICTIONS_FILE):
        os.remove(PREDICTIONS_FILE)
    yield
    # Limpiar después de la prueba también
    if os.path.exists(PREDICTIONS_FILE):
        os.remove(PREDICTIONS_FILE)


# ============================================================================
# PRUEBA 1: Verificar que el modelo retorna las 5 categorías correctamente
# ============================================================================
def test_modelo_cinco_categorias():
    """
    Prueba 1: Dados diferentes parámetros de entrada, verificar que el modelo
    puede retornar las 5 categorías de enfermedades.
    """
    # Caso 1: NO ENFERMO - Valores normales
    diagnostico1 = modelo_diagnostico(36.8, 75, 110)
    assert diagnostico1 == "NO ENFERMO", f"Esperado: NO ENFERMO, Obtenido: {diagnostico1}"
    
    # Caso 2: ENFERMEDAD LEVE - Fiebre ligera
    diagnostico2 = modelo_diagnostico(37.8, 105, 125)
    assert diagnostico2 == "ENFERMEDAD LEVE", f"Esperado: ENFERMEDAD LEVE, Obtenido: {diagnostico2}"
    
    # Caso 3: ENFERMEDAD CRÓNICA - Hipertensión moderada persistente
    diagnostico3 = modelo_diagnostico(37.0, 115, 145)
    assert diagnostico3 == "ENFERMEDAD CRÓNICA", f"Esperado: ENFERMEDAD CRÓNICA, Obtenido: {diagnostico3}"
    
    # Caso 4: ENFERMEDAD AGUDA - Fiebre alta y taquicardia
    diagnostico4 = modelo_diagnostico(40.0, 140, 170)
    assert diagnostico4 == "ENFERMEDAD AGUDA", f"Esperado: ENFERMEDAD AGUDA, Obtenido: {diagnostico4}"
    
    # Caso 5: ENFERMEDAD TERMINAL - Condiciones críticas múltiples
    diagnostico5 = modelo_diagnostico(41.5, 165, 190)
    assert diagnostico5 == "ENFERMEDAD TERMINAL", f"Esperado: ENFERMEDAD TERMINAL, Obtenido: {diagnostico5}"
    
    print("✅ Prueba 1 PASADA: Las 5 categorías son retornadas correctamente")


# ============================================================================
# PRUEBA 2: Verificar el sistema de reportes y estadísticas
# ============================================================================
def test_estadisticas_y_reporte(client, limpiar_predicciones):
    """
    Prueba 2: Verificar que el sistema de reportes funciona correctamente:
    - Inicialmente vacío
    - Después de predicciones, estadísticas correctas
    - Última predicción registrada correctamente
    """
    # Parte A: Verificar que inicialmente no hay predicciones
    response = client.get('/reporte')
    assert response.status_code == 200, f"Error al obtener reporte: {response.status_code}"
    
    data = json.loads(response.data)
    assert data['total_predicciones'] == 0, f"Total inicial debería ser 0, obtenido: {data['total_predicciones']}"
    assert data['fecha_ultima_prediccion'] is None, "Fecha inicial debería ser None"
    print("✅ Parte A PASADA: Reporte inicial vacío")
    
    # Parte B: Realizar 3 predicciones diferentes
    predicciones_a_realizar = [
        {'temperatura': 36.8, 'frecuencia_cardiaca': 75, 'presion_arterial': 110, 'esperado': 'NO ENFERMO'},
        {'temperatura': 37.8, 'frecuencia_cardiaca': 105, 'presion_arterial': 125, 'esperado': 'ENFERMEDAD LEVE'},
        {'temperatura': 41.5, 'frecuencia_cardiaca': 165, 'presion_arterial': 190, 'esperado': 'ENFERMEDAD TERMINAL'}
    ]
    
    for pred in predicciones_a_realizar:
        response = client.post('/predecir',
                              data=json.dumps({
                                  'temperatura': pred['temperatura'],
                                  'frecuencia_cardiaca': pred['frecuencia_cardiaca'],
                                  'presion_arterial': pred['presion_arterial']
                              }),
                              content_type='application/json')
        assert response.status_code == 200, f"Error al hacer predicción: {response.status_code}"
        
        data = json.loads(response.data)
        assert data['diagnostico'] == pred['esperado'], \
            f"Diagnóstico incorrecto. Esperado: {pred['esperado']}, Obtenido: {data['diagnostico']}"
    
    print("✅ Parte B PASADA: 3 predicciones realizadas correctamente")
    
    # Parte C: Verificar estadísticas después de las predicciones
    response = client.get('/reporte')
    assert response.status_code == 200, f"Error al obtener reporte: {response.status_code}"
    
    data = json.loads(response.data)
    
    # Verificar total de predicciones
    assert data['total_predicciones'] == 3, \
        f"Total debería ser 3, obtenido: {data['total_predicciones']}"
    
    # Verificar que hay al menos 3 categorías registradas
    categorias = data['predicciones_por_categoria']
    assert 'NO ENFERMO' in categorias, "Categoría NO ENFERMO no encontrada"
    assert 'ENFERMEDAD LEVE' in categorias, "Categoría ENFERMEDAD LEVE no encontrada"
    assert 'ENFERMEDAD TERMINAL' in categorias, "Categoría ENFERMEDAD TERMINAL no encontrada"
    
    assert categorias['NO ENFERMO'] == 1, f"Contador incorrecto para NO ENFERMO"
    assert categorias['ENFERMEDAD LEVE'] == 1, f"Contador incorrecto para ENFERMEDAD LEVE"
    assert categorias['ENFERMEDAD TERMINAL'] == 1, f"Contador incorrecto para ENFERMEDAD TERMINAL"
    
    # Verificar que hay fecha de última predicción
    assert data['fecha_ultima_prediccion'] is not None, "Debería haber fecha de última predicción"
    
    # Verificar últimas 5 predicciones (en este caso, las 3 realizadas)
    ultimas_5 = data['ultimas_5_predicciones']
    assert len(ultimas_5) == 3, f"Deberían haber 3 predicciones, obtenidas: {len(ultimas_5)}"
    
    # Verificar que la última predicción es ENFERMEDAD TERMINAL
    ultima_prediccion = ultimas_5[0]  # La primera en la lista es la más reciente
    assert ultima_prediccion['diagnostico'] == 'ENFERMEDAD TERMINAL', \
        f"Última predicción debería ser ENFERMEDAD TERMINAL, obtenida: {ultima_prediccion['diagnostico']}"
    
    print("✅ Parte C PASADA: Estadísticas correctas después de las predicciones")
    print("✅ Prueba 2 COMPLETA: Sistema de reportes funciona correctamente")


# ============================================================================
# PRUEBA ADICIONAL: Verificar endpoint de health check
# ============================================================================
def test_health_check(client):
    """
    Prueba adicional: Verificar que el endpoint de health check funciona
    """
    response = client.get('/health')
    assert response.status_code == 200, f"Health check falló con código: {response.status_code}"
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy', f"Status debería ser 'healthy', obtenido: {data['status']}"
    
    print("✅ Prueba Adicional PASADA: Health check funciona correctamente")


if __name__ == '__main__':
    # Ejecutar pruebas manualmente
    pytest.main([__file__, '-v', '-s'])

