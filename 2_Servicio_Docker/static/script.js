// Manejo del formulario de diagnóstico
document.getElementById('diagnosticoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Obtener valores del formulario
    const temperatura = document.getElementById('temperatura').value;
    const frecuencia_cardiaca = document.getElementById('frecuencia_cardiaca').value;
    const presion_arterial = document.getElementById('presion_arterial').value;
    
    // Mostrar loading
    document.querySelector('.loading').style.display = 'block';
    document.getElementById('resultado').style.display = 'none';
    
    try {
        // Realizar request al servidor
        const response = await fetch('/predecir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                temperatura: parseFloat(temperatura),
                frecuencia_cardiaca: parseInt(frecuencia_cardiaca),
                presion_arterial: parseInt(presion_arterial)
            })
        });
        
        const data = await response.json();
        
        // Ocultar loading
        document.querySelector('.loading').style.display = 'none';
        
        if (response.ok) {
            // Mostrar resultado
            const resultDiv = document.getElementById('resultado');
            const diagnosticoText = document.getElementById('diagnostico-text');
            
            diagnosticoText.textContent = data.diagnostico;
            
            // Remover clases anteriores
            resultDiv.classList.remove('no-enfermo', 'leve', 'aguda', 'cronica', 'terminal');
            
            // Agregar clase según diagnóstico
            if (data.diagnostico === 'NO ENFERMO') {
                resultDiv.classList.add('no-enfermo');
            } else if (data.diagnostico === 'ENFERMEDAD LEVE') {
                resultDiv.classList.add('leve');
            } else if (data.diagnostico === 'ENFERMEDAD AGUDA') {
                resultDiv.classList.add('aguda');
            } else if (data.diagnostico === 'ENFERMEDAD CRÓNICA') {
                resultDiv.classList.add('cronica');
            } else if (data.diagnostico === 'ENFERMEDAD TERMINAL') {
                resultDiv.classList.add('terminal');
            }
            
            resultDiv.style.display = 'block';
        } else {
            alert('Error: ' + (data.error || 'Error desconocido'));
        }
    } catch (error) {
        document.querySelector('.loading').style.display = 'none';
        alert('Error de conexión: ' + error.message);
    }
});

// Manejo del botón de reporte
document.getElementById('btnReporte').addEventListener('click', async function() {
    try {
        const response = await fetch('/reporte');
        const data = await response.json();
        
        if (response.ok) {
            mostrarReporte(data);
        } else {
            alert('Error al obtener el reporte');
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
});

// Botón cerrar reporte
document.getElementById('btnCerrarReporte').addEventListener('click', function() {
    document.getElementById('reporteSection').style.display = 'none';
});

// Función para mostrar el reporte
function mostrarReporte(data) {
    // Mostrar total de predicciones
    document.getElementById('totalPredicciones').textContent = data.total_predicciones;
    
    // Mostrar predicciones por categoría
    const categoriasDiv = document.getElementById('prediccionesPorCategoria');
    if (data.total_predicciones > 0) {
        let htmlCategorias = '';
        for (const [categoria, cantidad] of Object.entries(data.predicciones_por_categoria)) {
            const iconoCategoria = obtenerIconoCategoria(categoria);
            htmlCategorias += `
                <div class="categoria-item">
                    <span class="categoria-nombre">${iconoCategoria} ${categoria}</span>
                    <span class="categoria-cantidad">${cantidad}</span>
                </div>
            `;
        }
        categoriasDiv.innerHTML = htmlCategorias;
    } else {
        categoriasDiv.innerHTML = '<p class="no-data">No hay predicciones registradas</p>';
    }
    
    // Mostrar fecha última predicción
    const fechaDiv = document.getElementById('ultimaFecha');
    if (data.fecha_ultima_prediccion) {
        const fecha = new Date(data.fecha_ultima_prediccion);
        fechaDiv.textContent = fecha.toLocaleString('es-ES');
    } else {
        fechaDiv.textContent = '-';
    }
    
    // Mostrar últimas 5 predicciones
    const ultimas5Div = document.getElementById('ultimas5');
    if (data.ultimas_5_predicciones && data.ultimas_5_predicciones.length > 0) {
        let htmlUltimas = '';
        data.ultimas_5_predicciones.forEach((pred, index) => {
            const fecha = new Date(pred.timestamp);
            const iconoCategoria = obtenerIconoCategoria(pred.diagnostico);
            htmlUltimas += `
                <div class="prediccion-item">
                    <div class="prediccion-num">#${index + 1}</div>
                    <div class="prediccion-info">
                        <div class="prediccion-diagnostico">${iconoCategoria} ${pred.diagnostico}</div>
                        <div class="prediccion-parametros">
                            🌡️ ${pred.parametros.temperatura}°C | 
                            💓 ${pred.parametros.frecuencia_cardiaca} bpm | 
                            🩺 ${pred.parametros.presion_arterial} mmHg
                        </div>
                        <div class="prediccion-fecha">${fecha.toLocaleString('es-ES')}</div>
                    </div>
                </div>
            `;
        });
        ultimas5Div.innerHTML = htmlUltimas;
    } else {
        ultimas5Div.innerHTML = '<p class="no-data">No hay predicciones registradas</p>';
    }
    
    // Mostrar sección de reporte
    document.getElementById('reporteSection').style.display = 'block';
    document.getElementById('reporteSection').scrollIntoView({ behavior: 'smooth' });
}

// Función auxiliar para obtener iconos según categoría
function obtenerIconoCategoria(categoria) {
    const iconos = {
        'NO ENFERMO': '✅',
        'ENFERMEDAD LEVE': '⚠️',
        'ENFERMEDAD CRÓNICA': '🔶',
        'ENFERMEDAD AGUDA': '🔴',
        'ENFERMEDAD TERMINAL': '⚫'
    };
    return iconos[categoria] || '❓';
}

