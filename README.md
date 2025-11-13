# Proyecto Machine Learning - MLOps y Despliegue con Docker

**Autor:** Santiago Prado

---

## Problema

Desarrollar un sistema de Machine Learning para diagnóstico médico que permita clasificar el estado de salud de pacientes basándose en signos vitales (temperatura, frecuencia cardíaca y presión arterial). El sistema debe ser desplegado utilizando contenedores Docker para garantizar portabilidad y facilidad de despliegue.

---

## Propósito

Este proyecto tiene como objetivo:

1. **Implementar un pipeline de MLOps** completo para un sistema de diagnóstico médico, desde el diseño hasta la producción.

2. **Desarrollar un servicio web** utilizando Flask que simule un modelo de Machine Learning para clasificación de enfermedades.

3. **Containerizar la aplicación** con Docker para facilitar el despliegue y la escalabilidad del sistema.

4. **Clasificar pacientes** en 4 categorías según sus signos vitales:
   - NO ENFERMO
   - ENFERMEDAD LEVE
   - ENFERMEDAD AGUDA
   - ENFERMEDAD CRÓNICA

---

## Estructura del Repositorio

```
Projecto1 Machine Learning/
├── 1_Pipeline_MLOps/
│   ├── Diagrama Pipeline MLOps.jpg
│   └── Pipeline_MLOps_Diagnostico_Medico.md
│
├── 2_Servicio_Docker/
│   ├── app.py                    # Aplicación Flask
│   ├── Dockerfile                # Configuración Docker
│   ├── requirements.txt          # Dependencias Python
│   ├── templates/
│   │   └── index.html            # Interfaz web
│   └── static/
│       ├── style.css             # Estilos
│       └── script.js             # Lógica frontend
│
└── README.md                     # Este archivo
```

---

## Tecnologías Utilizadas

- **Python 3.11** - Lenguaje de programación
- **Flask 3.0** - Framework web
- **Docker** - Containerización
- **HTML/CSS/JavaScript** - Interfaz de usuario

---

## Repositorio

[GitHub - MLOps Medical Diagnosis System](https://github.com/santiagoprado21/MLOps-medical-diagnosis-system-with-Docker.git)
