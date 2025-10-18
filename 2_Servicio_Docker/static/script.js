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
            resultDiv.classList.remove('no-enfermo', 'leve', 'aguda', 'cronica');
            
            // Agregar clase según diagnóstico
            if (data.diagnostico === 'NO ENFERMO') {
                resultDiv.classList.add('no-enfermo');
            } else if (data.diagnostico === 'ENFERMEDAD LEVE') {
                resultDiv.classList.add('leve');
            } else if (data.diagnostico === 'ENFERMEDAD AGUDA') {
                resultDiv.classList.add('aguda');
            } else if (data.diagnostico === 'ENFERMEDAD CRÓNICA') {
                resultDiv.classList.add('cronica');
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

