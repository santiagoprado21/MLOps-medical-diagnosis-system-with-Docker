# Proyecto Machine Learning - MLOps y Despliegue con Docker
**Autor:** Santiago Prado

---

## Descripción del Proyecto

Este proyecto contiene:

1. **Pipeline de MLOps** - Diseño end-to-end para sistema de diagnóstico médico
2. **Servicio Docker** - Aplicación Flask que simula un modelo ML de clasificación

---

## Estructura del Proyecto

```
Projecto1 Machine Learning/
├── 1_Pipeline_MLOps/
│   └── Pipeline_MLOps_Diagnostico_Medico.md    # Diagrama y explicación del pipeline
│
├── 2_Servicio_Docker/
│   ├── app.py                                   # Aplicación Flask (Backend)
│   ├── Dockerfile                               # Configuración Docker
│   ├── requirements.txt                         # Dependencias Python
│   ├── templates/
│   │   └── index.html                           # Estructura HTML
│   └── static/
│       ├── style.css                            # Estilos CSS
│       └── script.js                            # Lógica JavaScript
│
└── README.md                                    # Este archivo
```

---

## Parte 1: Pipeline de MLOps

Contiene:
- Diagrama visual del pipeline (enlace a Miro)
- Explicación de las 3 fases: Diseño, Desarrollo, Producción

---

## Parte 2: Servicio Docker

### Descripción

Sistema que clasifica pacientes en 4 categorías según signos vitales:
- **NO ENFERMO**
- **ENFERMEDAD LEVE**
- **ENFERMEDAD AGUDA**
- **ENFERMEDAD CRÓNICA**

**Parámetros de entrada:**
1. Temperatura corporal (°C)
2. Frecuencia cardíaca (bpm)
3. Presión arterial sistólica (mmHg)

---

## Instrucciones de Docker

### Pre-requisito: Instalar Docker

# Verificar instalación:

```bash
docker --version

```
### Construcción de la Imagen

```bash
# Navegar al directorio del servicio
cd 2_Servicio_Docker

# Construir la imagen
docker build -t medico:1.0 .
```

### Ejecución del Contenedor

```bash
# Ejecutar el contenedor
docker run -d -p 5000:5000 --name medico-service medico:1.0
```

**Parámetros:**
- `-d`: Ejecuta en background
- `-p 5000:5000`: Mapea el puerto 5000
- `--name medico-service`: Asigna nombre al contenedor

### Uso del Servicio

**Interfaz Web:**
- Abrir en navegador: `http://localhost:5000`
- Ingresar los 3 valores (temperatura, frecuencia cardíaca, presión arterial)
- Presionar "Realizar Diagnóstico"
- Ver el resultado en pantalla

### Comandos Útiles

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del contenedor
docker logs medico-service

# Detener el contenedor
docker stop medico-service

# Iniciar contenedor detenido
docker start medico-service

# Eliminar el contenedor
docker rm medico-service

# Eliminar la imagen
docker rmi medico:1.0
```

---

## Pruebas de los 4 Estados

El servicio puede retornar los 4 diagnósticos posibles:

| Temperatura | FC  | PA  | Diagnóstico           |
|-------------|-----|-----|-----------------------|
| 36.8°C      | 75  | 110 | NO ENFERMO            |
| 37.8°C      | 105 | 125 | ENFERMEDAD LEVE       |
| 39.5°C      | 135 | 165 | ENFERMEDAD AGUDA      |
| 37.0°C      | 115 | 145 | ENFERMEDAD CRÓNICA    |

**Probar todos los casos:**
```bash
curl http://localhost:5000/test
```

---

## Tecnologías

- Python 3.11
- Flask 3.0
- Docker
- HTML/CSS/JavaScript

---

Link a GitHub:

https://github.com/santiagoprado21/MLOps-medical-diagnosis-system-with-Docker.git

