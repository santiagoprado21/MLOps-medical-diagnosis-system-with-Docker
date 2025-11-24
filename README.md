# MLOps Pipeline Design - Sistema de Diagnóstico de Enfermedades → V2.0

**Autor:** Santiago Prado

---

## Case Challenge

### Background

En el campo médico, la abundancia de información de pacientes contrasta con la escasez de datos para enfermedades huérfanas (raras). Esta asimetría representa un desafío significativo para el desarrollo de sistemas de diagnóstico asistido por ML. Un sistema efectivo debe ser capaz de predecir enfermedades tanto comunes (con millones de registros) como huérfanas (con cientos o pocos miles de casos), manteniendo altos estándares de precisión clínica y cumplimiento normativo.

### Problem Definition

#### Objective

Construir un modelo de Machine Learning que, dados los datos de síntomas y características clínicas de un paciente, sea capaz de predecir la probabilidad de que este sufra alguna enfermedad, clasificándola en una de las posibles categorías del sistema. El modelo debe funcionar eficientemente tanto para enfermedades comunes como para enfermedades huérfanas.

#### Deployment Requirements

El sistema debe ofrecer flexibilidad en su despliegue:

- **Escenario Local:** El médico puede ejecutar el modelo en su computador local (laptop/desktop) sin conexión a internet, ideal para consultorios con recursos computacionales moderados y restricciones de conectividad.

- **Escenario Cloud:** El médico puede realizar consultas al modelo mediante una API REST si este está alojado en un servicio en la nube o servidor institucional, permitiendo centralizar actualizaciones y aprovechar mayor poder computacional.

---

## Part 1: Machine Learning Pipeline Design

De acuerdo con los requerimientos del problema de clasificación médica, se propone el siguiente pipeline de MLOps:

![ML Pipeline](imgs/Diagrama%20End-to-End%20ML.png)

> **Nota sobre el diagrama:** La Fase 3 (Producción y Monitoreo) aparece condensada en el diagrama debido a limitaciones de la versión gratuita de Lucidchart en cuanto al número de formas permitidas. Las secciones siguientes describen en detalle todos los componentes de cada fase, incluyendo los 6 componentes específicos de la Fase 3 (Containerización, Deployment, CI/CD, Model Serving, Monitoring y Feedback Loop).

Las siguientes secciones explican en detalle el pipeline propuesto.

---

### FASE 1: DISEÑO Y PREPARACIÓN

Esta fase inicial es crítica para establecer las bases del proyecto. Incluye la definición de requerimientos, identificación de fuentes de datos y diseño arquitectónico del sistema.

---

#### Análisis de Requerimientos Clínicos y Regulatorios

Antes de iniciar el desarrollo, es fundamental comprender el contexto médico-legal en el que operará el sistema. Se deben establecer:

- **Requerimientos clínicos:** Definición de las métricas que realmente importan en medicina (sensibilidad, especificidad, valores predictivos positivos y negativos). A diferencia de problemas genéricos de clasificación, en medicina un falso negativo puede tener consecuencias graves, por lo que la sensibilidad suele priorizarse.

- **Restricciones regulatorias:** El sistema debe cumplir con normativas como HIPAA (EE.UU.), GDPR (Europa), o regulaciones locales de protección de datos médicos. Esto implica encriptación de datos, trazabilidad de accesos, y anonimización cuando sea necesario.

- **Niveles de servicio (SLA):** Definir tiempos de respuesta aceptables, disponibilidad del sistema (99.9% uptime para sistemas críticos), y protocolos de contingencia.

La interpretabilidad del modelo es crucial. Los médicos necesitan entender por qué el modelo sugiere cierto diagnóstico, por lo que técnicas como SHAP o LIME deben considerarse desde el diseño.

---

#### Identificación de Tipos de Datos Disponibles

Los datos médicos son heterogéneos y provienen de múltiples fuentes:

- **Datos estructurados:** Edad, género, peso, altura, resultados de laboratorio (glucosa, colesterol, hemoglobina), signos vitales (presión arterial, frecuencia cardíaca, temperatura). Estos datos suelen venir de sistemas hospitalarios (EHR - Electronic Health Records) y son relativamente fáciles de procesar.

- **Datos semi-estructurados:** Registros médicos en formatos JSON o XML, historiales de medicamentos, resultados de estudios de imagen con metadata. Requieren parsing y normalización antes de ser utilizados.

- **Datos no estructurados:** Notas clínicas escritas por médicos, descripciones de síntomas por parte del paciente, informes de radiología en texto libre. Estos datos son valiosos pero requieren técnicas de NLP (Natural Language Processing) para su procesamiento.

**Suposición importante:** Para este proyecto, asumimos que tenemos acceso a bases de datos médicas públicas como MIMIC-III, UK Biobank, o similares para enfermedades comunes, y datasets especializados más pequeños para enfermedades huérfanas. También asumimos que los datos han sido previamente anonimizados cumpliendo con regulaciones de privacidad.

---

#### Diseño de Arquitectura del Sistema

El diseño arquitectónico debe soportar ambos escenarios de deployment:

**Arquitectura Híbrida:** El sistema se diseña como una aplicación containerizada que puede ejecutarse localmente o desplegarse en la nube. Esto se logra mediante Docker, que empaqueta el modelo, sus dependencias, y una interfaz de predicción en un contenedor portable.

- Para el **escenario local**, el contenedor se ejecuta en Docker Desktop con una interfaz web simple accesible vía localhost. Los logs y predicciones se almacenan localmente en SQLite.

- Para el **escenario cloud**, el mismo contenedor se despliega en servicios como AWS ECS, Azure Container Instances, o Kubernetes clusters (EKS/AKS/GKE). Se expone una API REST con autenticación, y los logs se centralizan en servicios como CloudWatch o Azure Monitor.

**Tecnologías principales:** Docker para containerización, FastAPI o Flask para el servidor web, y GitHub como repositorio central con GitHub Actions para CI/CD.

---

#### Estrategia para Enfermedades Huérfanas

Las enfermedades huérfanas presentan un desafío único: pocos datos de entrenamiento. La estrategia tradicional de "más datos = mejor modelo" no aplica aquí. Se proponen técnicas especializadas:

- **Few-Shot Learning:** Modelos capaces de aprender de pocos ejemplos (5-50 casos por clase). Algoritmos como Prototypical Networks o Matching Networks son candidatos.

- **Transfer Learning:** Usar modelos pre-entrenados en enfermedades comunes y afinarlos (fine-tuning) con los pocos datos de enfermedades huérfanas. La hipótesis es que patrones clínicos generales (fiebre, inflamación, etc.) son transferibles.

- **Data Augmentation:** Técnicas para generar variaciones sintéticas de los datos existentes sin alterar la validez médica. Por ejemplo, SMOTE para datos tabulares, o técnicas de text augmentation para notas clínicas.

- **Meta-Learning:** Entrenar un modelo para "aprender a aprender", de modo que cuando se presente una nueva enfermedad huérfana, el modelo pueda adaptarse rápidamente con pocos ejemplos.

**Tecnologías:** PyTorch o TensorFlow para implementar estas arquitecturas avanzadas, bibliotecas especializadas como `learn2learn` para meta-learning.

---

### FASE 2: DESARROLLO Y ENTRENAMIENTO

En esta fase se construye el pipeline de datos y se desarrollan los modelos de Machine Learning. Es la etapa más iterativa del proceso.

---

#### Ingesta y Almacenamiento de Datos

Los datos médicos deben ser ingestados desde múltiples fuentes y almacenados de forma estructurada y versionada.

**Ingesta:** Los datos pueden provenir de APIs de sistemas hospitalarios (HL7/FHIR estándares), archivos CSV/JSON exportados, o bases de datos relacionales. Se implementan scripts de ETL (Extract, Transform, Load) para normalizar formatos.

**Almacenamiento:** 
- **Raw Data Lake:** AWS S3 o Azure Blob Storage para almacenar datos en su forma original. Esto permite auditorías y reprocesamiento futuro.
- **Processed Data Warehouse:** Amazon Redshift, Google BigQuery, o PostgreSQL para datos limpios y listos para entrenamiento. Facilita consultas SQL eficientes.
- **Versionamiento:** DVC (Data Version Control) se utiliza para versionar datasets. Cada experimento queda asociado a una versión específica de datos, garantizando reproducibilidad.

**Tecnologías:** AWS S3/Azure Blob, DVC, PostgreSQL/MongoDB, scripts en Python con Pandas.

---

#### Preprocesamiento y Feature Engineering

Los datos médicos crudos rara vez están listos para entrenamiento. Esta etapa es crucial:

**Limpieza:** Imputación de valores faltantes (común en datos médicos), detección y manejo de outliers, corrección de inconsistencias (ej: fechas inválidas).

**Normalización:** Estandarización de unidades (kg vs lbs, °C vs °F), escalado de features numéricas (StandardScaler, MinMaxScaler).

**Feature Engineering:**
- Para datos estructurados: creación de features derivadas (IMC = peso/altura², rangos de normalidad para laboratorios).
- Para texto clínico: embeddings usando modelos pre-entrenados en textos médicos como BioBERT o ClinicalBERT. Estos modelos de NLP capturan el contexto médico mejor que BERT genérico.
- Agregaciones temporales: si hay datos longitudinales (múltiples visitas), calcular tendencias (ej: cambio en glucosa en últimos 6 meses).

**Feature Selection:** Técnicas como LASSO, Random Forest feature importance, o análisis de correlación para reducir dimensionalidad y evitar overfitting.

**Tecnologías:** Pandas, NumPy, Scikit-learn, spaCy, transformers (Hugging Face) para NLP, Jupyter Notebooks para exploración.

---

#### Entrenamiento y Validación de Modelos

Se entrenan múltiples modelos en paralelo para comparar desempeño:

**Para enfermedades comunes (datos abundantes):**
- **Gradient Boosting:** XGBoost, LightGBM, CatBoost. Excelentes para datos tabulares, interpretables, y eficientes.
- **Random Forests:** Robustos y ofrecen feature importance nativo.
- **Neural Networks:** MLPs o arquitecturas más complejas si hay suficiente data y recursos computacionales.

**Para enfermedades huérfanas (pocos datos):**
- **Prototypical Networks:** Aprenden representaciones donde ejemplos de la misma clase se agrupan.
- **Siamese Networks:** Aprenden similaridad entre casos, útil cuando hay pocos ejemplos por clase.
- **Transfer Learning:** Fine-tuning de modelos entrenados en enfermedades comunes.

**Validación:** 
- K-Fold Cross-Validation (k=5 o k=10) para asegurar que el modelo generaliza.
- Stratified sampling para mantener proporciones de clases, especialmente importante en datos médicos desbalanceados.
- Validación temporal: si los datos tienen timestamps, validar con datos futuros para simular uso real.

**Frameworks:** Scikit-learn para algoritmos clásicos, PyTorch o TensorFlow para deep learning, Jupyter Notebooks o scripts Python versionados en Git.

---

#### Experiment Tracking y Registro de Modelos

Con múltiples experimentos (distintos hiperparámetros, features, modelos), es fácil perder track. Experiment tracking es esencial:

**MLflow:** Herramienta open-source que permite:
- Logging automático de parámetros (learning rate, max_depth, etc.)
- Logging de métricas (accuracy, AUC, F1, sensibilidad, especificidad)
- Almacenamiento de artifacts (modelos serializados, gráficos de confusion matrix, curvas ROC)
- Comparación visual de experimentos en UI web

**Model Registry:** Una vez un modelo pasa las pruebas, se registra en MLflow Model Registry con estados (Staging, Production, Archived). Esto permite trazabilidad: saber exactamente qué modelo está en producción, con qué datos fue entrenado, y qué métricas obtuvo.

**Alternativas:** Weights & Biases (más orientado a deep learning), Neptune.ai, o soluciones cloud-native como AWS SageMaker Experiments.

**Tecnologías:** MLflow (principal), configurado con backend en S3 para artifacts y PostgreSQL para metadata.

---

#### Model Evaluation y Selección

Antes de llevar un modelo a producción, debe pasar rigurosa evaluación:

**Métricas Clínicas:**
- **Sensibilidad (Recall):** % de enfermos correctamente identificados. Crítico en medicina: preferimos falsos positivos a falsos negativos.
- **Especificidad:** % de sanos correctamente identificados. Importante para no alarmar innecesariamente.
- **Precision (PPV):** De los que predecimos enfermos, cuántos realmente lo están.
- **F1-Score:** Balance entre precision y recall.
- **AUC-ROC:** Capacidad del modelo de discriminar entre clases.

**Interpretabilidad:** SHAP (SHapley Additive exPlanations) para explicar predicciones individuales. Un médico puede ver: "El modelo sugiere diabetes con 85% de probabilidad porque la glucosa está en 180 mg/dL (contribución +0.4), el IMC es 32 (contribución +0.2), y hay historial familiar (contribución +0.15)".

**Validación con Expertos:** Idealmente, médicos especialistas revisan casos de prueba y validan si las predicciones tienen sentido clínico. Esto es especialmente importante para enfermedades huérfanas donde el modelo puede cometer errores sutiles.

**Criterios de Aprobación:** El modelo debe superar un umbral mínimo (ej: sensibilidad > 90% para enfermedades graves) y ser interpretable antes de pasar a producción.

Si el modelo no cumple criterios, se regresa a la etapa de entrenamiento para ajustar features, hiperparámetros, o incluso cambiar de algoritmo.

**Tecnologías:** Scikit-learn metrics, SHAP, matplotlib/seaborn para visualizaciones, Streamlit para dashboards interactivos.

---

### FASE 3: PRODUCCIÓN Y MONITOREO

Una vez el modelo está validado, se despliega en producción y se monitorea continuamente.

---

#### Containerización y Empaquetado del Modelo

El modelo entrenado debe empaquetarse para ser portable y reproducible:

**Serialización:** El modelo se serializa usando pickle, joblib, o ONNX (este último permite interoperabilidad entre frameworks). Se guarda junto con el preprocessor (scaler, encoder) para que la pipeline completa esté contenida.

**Docker Container:** Se crea un Dockerfile que:
- Parte de una imagen base ligera (Python 3.11-slim)
- Instala dependencias desde requirements.txt
- Copia el modelo serializado
- Expone un servidor web (FastAPI) con endpoints de predicción
- Incluye health checks para Kubernetes

Este contenedor es idéntico en desarrollo, staging y producción, eliminando el clásico "en mi máquina funciona".

**Tecnologías:** Docker, FastAPI (más moderno y rápido que Flask), Pydantic para validación de inputs.

---

#### Deployment - Estrategia Dual

**Opción 1: Deployment Local (Offline)**

Para médicos en zonas con conectividad limitada o que prefieren autonomía:

- El contenedor Docker se distribuye como un ejecutable que se instala vía Docker Desktop.
- La interfaz web corre en `localhost:5000` con una UI simple pero funcional.
- Predicciones y logs se guardan localmente en SQLite.
- Actualizaciones se distribuyen como nuevas versiones del contenedor (descargables o vía USB en zonas muy remotas).

**Ventajas:** No depende de internet, datos sensibles nunca salen del consultorio, sin costos cloud recurrentes.

**Desventajas:** Actualizaciones manuales, no se captura feedback centralizado fácilmente.

**Opción 2: Deployment Cloud (Online)**

Para hospitales o clínicas con infraestructura:

- El contenedor se despliega en Kubernetes (AWS EKS, Azure AKS, Google GKE) para orquestación.
- Auto-scaling: si hay picos de demanda, se levantan más pods automáticamente.
- Load Balancer distribuye requests entre múltiples instancias.
- API REST accesible vía HTTPS con autenticación JWT.
- Centralización de logs, métricas, y feedback de usuarios.

**Ventajas:** Actualizaciones instantáneas para todos los usuarios, mejor monitoreo, escalabilidad ilimitada.

**Desventajas:** Requiere conexión estable, costos cloud, mayor complejidad.

**Tecnologías:** Docker, Kubernetes, AWS ECS/EKS o Azure Container Instances/AKS, Terraform para Infrastructure as Code.

---

#### CI/CD Pipeline

GitHub Actions automatiza todo el proceso desde commit hasta deployment:

**Pipeline de CI (Continuous Integration):**
1. Al hacer push, se ejecutan tests unitarios del código.
2. Linting y formatting (flake8, black) para mantener calidad de código.
3. Security scans (Bandit, safety) para detectar vulnerabilidades en dependencias.
4. Model validation: cargar el modelo y hacer predicciones de prueba para asegurar que no está corrupto.

**Pipeline de CD (Continuous Deployment):**
1. Si pasan todos los tests, se construye la imagen Docker.
2. La imagen se sube a un registry (Docker Hub, AWS ECR, GitHub Container Registry).
3. Se despliega automáticamente a un ambiente de staging.
4. Tras aprobación manual (o automática si hay suficiente confianza), se despliega a producción.

**Tecnologías:** GitHub Actions (ya configurado en `.github/workflows/`), Docker, scripts de deployment.

---

#### Model Serving

El modelo expuesto via API REST debe ser robusto y bien documentado:

**Endpoints principales:**
- `POST /predict`: Recibe datos del paciente (JSON), retorna predicción con probabilidades y explicación SHAP.
- `GET /health`: Health check para Kubernetes/load balancers.
- `GET /model-info`: Retorna metadata del modelo (versión, fecha de entrenamiento, métricas).
- `POST /feedback`: Permite al médico reportar si la predicción fue correcta o no (para reentrenamiento futuro).

**FastAPI** genera documentación Swagger automáticamente en `/docs`, permitiendo a developers probar la API interactivamente.

**Rate limiting y autenticación:** Nginx o API Gateway para evitar abuso, JWT tokens para autenticación.

**Tecnologías:** FastAPI, Uvicorn (ASGI server), Nginx, AWS API Gateway o Azure API Management.

---

#### Monitoring y Observability

Un modelo en producción puede degradarse silenciosamente. El monitoreo continuo es crítico:

**Model Performance Monitoring:**
- **Evidently AI:** Detecta data drift (cuando la distribución de datos de entrada cambia) y concept drift (cuando la relación entre features y target cambia).
- Si la sensibilidad cae por debajo del umbral, se genera alerta.
- A/B testing: si hay un nuevo modelo, se puede servir al 10% de tráfico para comparar con el modelo actual.

**Infrastructure Monitoring:**
- **Prometheus + Grafana:** Métricas de infraestructura (CPU, memoria, latencia de requests, tasa de errores).
- CloudWatch (AWS) o Azure Monitor para logs centralizados.
- Dashboards muestran en tiempo real el estado del sistema.

**Alerting:**
- Alertas vía Slack/Email si la latencia supera 500ms, si la tasa de errores sube, o si se detecta drift.
- PagerDuty para alertas críticas 24/7.

**Tecnologías:** Evidently AI, Prometheus, Grafana, CloudWatch/Azure Monitor, Slack webhooks.

---

#### Feedback Loop y Reentrenamiento Continuo

El modelo debe mejorar con el tiempo:

**Captura de Feedback:**
- Cada predicción se loggea junto con el outcome real (si el médico lo reporta).
- Casos donde el modelo falló se marcan para revisión.

**Detección de Degradación:**
- Si el drift supera umbral o las métricas caen, se activa trigger de reentrenamiento.

**Reentrenamiento Automatizado:**
- Un Airflow DAG (o GitHub Action programada) se ejecuta mensualmente o cuando se detecta drift.
- Retoma datos actualizados (incluyendo feedback), reentrena el modelo, lo evalúa en validation set.
- Si el nuevo modelo supera al anterior, se sube a Model Registry como candidato.
- Tras aprobación (manual o automática según confianza), se despliega vía CI/CD.

Este ciclo cerrado asegura mejora continua sin intervención humana constante.

**Tecnologías:** Airflow (opcional, para workflows complejos), GitHub Actions, scripts Python, MLflow para comparar modelos.

---

## Part 2: Consideraciones Especiales del Problema

### Manejo del Desbalance de Datos

Las enfermedades huérfanas por definición tienen pocos casos. Técnicas para mitigar:

- **Class Weighting:** En el loss function, dar mayor peso a clases minoritarias.
- **SMOTE:** Synthetic Minority Over-sampling Technique, genera ejemplos sintéticos de la clase minoritaria.
- **Ensemble de Modelos:** Un modelo general para enfermedades comunes, y modelos especializados (few-shot) para cada enfermedad huérfana. Un router decide qué modelo usar.

### Seguridad y Privacidad

Datos médicos son ultra-sensibles:

- **Encriptación:** TLS para datos en tránsito, encriptación at-rest en S3/databases.
- **Anonimización:** Remover PII (Personally Identifiable Information) antes de entrenamiento. Técnicas como k-anonymity.
- **Auditoría:** Logs de quién accedió a qué datos y cuándo.
- **Cumplimiento:** HIPAA audits anuales, GDPR compliance con derecho al olvido (si un paciente pide eliminar sus datos, deben removerse del training set, requiriendo reentrenamiento).

### Escalabilidad

Si el sistema crece a millones de usuarios:

- Kubernetes auto-scaling maneja carga variable.
- Model serving en GPU (AWS Inferentia, NVIDIA Triton) para modelos grandes de deep learning.
- Caching de predicciones para casos repetidos (ej: chequeos rutinarios).
- Edge deployment: modelos cuantizados desplegados en dispositivos móviles para consultorios muy remotos.

---

## Part 3: Escenarios Futuros y Adaptabilidad

El pipeline propuesto es flexible y puede adaptarse a nuevos requerimientos:

### Predicciones en Tiempo Real (<1 segundo)

Si se requiere diagnóstico instantáneo (ej: emergencias):

- Optimización del modelo: cuantización (reducir precisión de float32 a int8), pruning (eliminar neuronas innecesarias).
- Deployment en GPUs o FPGAs.
- Caching agresivo.
- Load balancers con múltiples réplicas.

El pipeline actual ya soporta esto con FastAPI + Kubernetes escalable.

### Reentrenamiento con Feedback de Usuarios

Ya contemplado en el feedback loop. Puede extenderse con:

- Active Learning: el modelo identifica casos de los que está menos seguro y pide al médico etiquetarlos prioritariamente.
- Reinforcement Learning from Human Feedback (RLHF): el modelo aprende no solo de etiquetas, sino de preferencias (ej: médico prefiere diagnóstico A sobre B para este caso).

### Multi-Modelo por Especialidad

En lugar de un modelo monolítico:

- Modelo de cardiología para enfermedades cardíacas.
- Modelo de neurología para enfermedades neurológicas.
- Un router (modelo de clasificación simple) decide qué modelo especializado consultar.

Esto mejora precisión y permite equipos especializados manejar su propio modelo.

MLflow Model Registry y Kubernetes soportan servir múltiples modelos simultáneamente.

### Integración con Sistemas Hospitalarios

Para uso en hospitales grandes:

- Integración vía APIs estándar HL7 FHIR (interoperabilidad con sistemas EHR como Epic, Cerner).
- SSO (Single Sign-On) para autenticación integrada.
- Compliance con frameworks de seguridad hospitalaria.

El diseño API-first del pipeline facilita estas integraciones.

---

## Tecnologías Principales - Stack Completo

### Fase de Diseño
- **Documentación:** Markdown, Draw.io
- **Versionamiento:** Git, GitHub

### Fase de Desarrollo
- **Lenguaje:** Python 3.10+
- **Data Storage:** AWS S3, PostgreSQL, MongoDB
- **Data Versioning:** DVC
- **Data Processing:** Pandas, NumPy, Scikit-learn
- **NLP:** spaCy, transformers (BioBERT, ClinicalBERT)
- **ML Frameworks:** Scikit-learn, XGBoost, LightGBM, PyTorch, TensorFlow
- **Experiment Tracking:** MLflow
- **Development Environment:** Jupyter Notebooks, VS Code

### Fase de Producción
- **Containerización:** Docker
- **Orquestación:** Kubernetes (EKS/AKS/GKE)
- **API Framework:** FastAPI
- **CI/CD:** GitHub Actions
- **Monitoring:** Evidently AI, Prometheus, Grafana, CloudWatch
- **Logging:** CloudWatch, Azure Monitor
- **Infrastructure as Code:** Terraform
- **Alerting:** Slack, PagerDuty

### Opcional/Avanzado
- **Workflow Orchestration:** Apache Airflow (para pipelines complejos)
- **Advanced ML Platform:** AWS SageMaker (si el presupuesto lo permite)
- **Model Optimization:** ONNX Runtime, TensorRT

---

## Suposiciones Principales

1. **Disponibilidad de Datos:** Asumimos acceso a datasets médicos públicos o institucionales con al menos 10,000 registros para enfermedades comunes y 50-500 para enfermedades huérfanas.

2. **Anonimización Previa:** Los datos ya cumplen con regulaciones de privacidad. Si no, se requiere una etapa adicional de anonimización.

3. **Infraestructura Cloud:** Para el escenario online, asumimos presupuesto para servicios cloud (AWS/Azure/GCP). Estimado: $500-2000/mes dependiendo de escala.

4. **Expertise Médico:** Disponibilidad de médicos especialistas para validar modelos y proveer feedback, especialmente para enfermedades huérfanas.

5. **Recursos Computacionales:** Para entrenamiento, acceso a instancias con GPU (AWS p3.2xlarge o similar) para modelos de deep learning. Para enfermedades comunes con métodos clásicos, CPUs suficientes.

6. **Actualización de Modelos:** El modelo se reentrena mensualmente o cuando se detecta drift significativo, no en tiempo real por cada predicción.

7. **Latencia Aceptable:** Asumimos que 1-3 segundos de latencia para obtener una predicción es aceptable. Si se requiere <1s, se necesitan optimizaciones adicionales.

8. **Interpretabilidad:** Priorizamos modelos interpretables (tree-based) sobre cajas negras (deep learning) excepto cuando la complejidad del problema lo justifica.

---

## Conclusión

Este pipeline MLOps presenta una solución end-to-end para el desafío de diagnóstico de enfermedades comunes y huérfanas. Desde el diseño consciente de restricciones médico-legales, pasando por técnicas especializadas de few-shot learning, hasta un deployment flexible (local y cloud) con monitoreo continuo y feedback loop, el sistema está preparado para operar en producción de manera confiable, escalable y en constante mejora.

La elección de tecnologías balances madurez (Docker, Kubernetes, Scikit-learn), innovación (Evidently AI para drift detection, few-shot learning), y pragmatismo (FastAPI por su simplicidad, MLflow por ser open-source). El resultado es un pipeline robusto, bien documentado y listo para ser implementado por un equipo de ML.

---

## Repositorio

[GitHub - MLOps Medical Diagnosis System](https://github.com/santiagoprado21/MLOps-medical-diagnosis-system-with-Docker.git)

**Autor:** Santiago Prado  
**Fecha:** Noviembre 2025  
**Versión:** 2.0
