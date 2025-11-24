# CHANGELOG - Pipeline MLOps Sistema de Diagnóstico de Enfermedades

## Comparación: Versión 1.0 (Inicial) vs Versión 2.0 (Actual)

Este documento detalla los cambios, mejoras y adiciones realizadas al pipeline MLOps entre la propuesta inicial (Semana 1) y la propuesta actual (Semana 11), reflejando el conocimiento adquirido durante el curso.

---

## [Version 2.0] - Noviembre 2025

### ✅ ADDED - Nuevos Componentes y Etapas

#### Fase de Diseño
- **Estrategia específica para enfermedades huérfanas:** Se añadió una sub-etapa completa dedicada a técnicas de Few-Shot Learning, Meta-Learning, Transfer Learning y Data Augmentation para manejar el desafío de pocos datos.
- **Análisis de tipos de datos:** Se expandió la identificación de fuentes de datos, clasificándolas en estructurados, semi-estructurados y no estructurados, con estrategias específicas para cada tipo.
- **Arquitectura híbrida detallada:** Se especificó claramente cómo soportar deployment local (offline) y cloud (online) desde el diseño arquitectónico.

#### Fase de Desarrollo
- **Data Version Control (DVC):** Se incorporó DVC para versionamiento de datasets, garantizando reproducibilidad completa de experimentos.
- **Experiment Tracking con MLflow:** Se añadió MLflow como herramienta central para tracking de experimentos, logging de métricas y parámetros, y gestión de artifacts.
- **Model Registry:** Se implementa un registro centralizado de modelos con estados (Staging, Production, Archived) usando MLflow Model Registry.
- **NLP para datos médicos:** Se añadió procesamiento de lenguaje natural con modelos especializados (BioBERT, ClinicalBERT) para notas clínicas y texto libre.
- **Feature Engineering avanzado:** Se detallaron técnicas específicas como creación de embeddings, agregaciones temporales, y feature selection.
- **Interpretabilidad con SHAP:** Se incorporó SHAP para explicar predicciones individuales, crítico en contexto médico.
- **Validación con expertos:** Se añadió validación clínica con médicos especialistas como paso previo a producción.

#### Fase de Producción
- **Containerización con Docker:** Se especifica la creación de contenedores Docker para portabilidad completa del modelo.
- **CI/CD completo con GitHub Actions:** Se detalla un pipeline automatizado de integración y despliegue continuo con tests, linting, security scans y deployment automatizado.
- **Kubernetes para orquestación:** Se añadió orquestación con Kubernetes (EKS/AKS/GKE) para escalabilidad y alta disponibilidad en el escenario cloud.
- **API REST con FastAPI:** Se especifica FastAPI como framework para exposición del modelo vía API con documentación Swagger automática.
- **Model Monitoring con Evidently AI:** Se incorporó detección automática de data drift y concept drift.
- **Observability Stack:** Se añadió stack completo de monitoreo (Prometheus + Grafana) y logging centralizado (CloudWatch/Azure Monitor).
- **Alerting:** Sistema de alertas vía Slack/Email/PagerDuty para respuesta rápida ante degradación.
- **Feedback Loop:** Se diseñó un ciclo cerrado de feedback que captura predicciones incorrectas y activa reentrenamiento automático.

#### Documentación y Suposiciones
- **Sección de Suposiciones:** Se añadió sección explícita documentando todas las suposiciones (disponibilidad de datos, infraestructura, recursos computacionales, latencia aceptable, etc.).
- **Escenarios Futuros (Part 3):** Se añadió sección completa sobre adaptabilidad del pipeline a nuevos requerimientos (tiempo real, multi-modelo, integración hospitalaria).
- **Stack Tecnológico Completo:** Se documentó el stack completo de tecnologías con justificación para cada herramienta.

---

### 🔄 CHANGED - Modificaciones Significativas

#### De Propuesta General a Especificación Detallada
- **Versión 1.0:** Las tres fases (Diseño, Desarrollo, Producción) estaban descritas en párrafos generales de 3-4 líneas cada una.
- **Versión 2.0:** Cada fase se expande en múltiples sub-etapas con explicaciones detalladas de 5-10 párrafos, incluyendo justificaciones técnicas y médicas.

#### Ingesta y Almacenamiento
- **Versión 1.0:** "Ingesta y almacenamiento de datos clínicos desde múltiples fuentes."
- **Versión 2.0:** Se especifica arquitectura Data Lake (S3/Azure Blob) + Data Warehouse (Redshift/BigQuery), con DVC para versionamiento. Se detalla ETL desde APIs HL7/FHIR, archivos CSV/JSON, y bases de datos relacionales.

#### Preprocesamiento
- **Versión 1.0:** "Preprocesamiento: limpieza, normalización y creación de variables relevantes."
- **Versión 2.0:** Se detalla imputación de valores faltantes, detección de outliers, normalización de unidades, feature engineering específico (IMC, tendencias temporales), NLP con BioBERT para texto clínico, y feature selection con múltiples técnicas (LASSO, Random Forest importance).

#### Entrenamiento y Validación
- **Versión 1.0:** "Entrenamiento y validación: uso de modelos interpretables (XGBoost, Random Forest) con métricas clínicas y validación cruzada."
- **Versión 2.0:** Se especifican:
  - **Dos tracks separados:** Modelos clásicos (XGBoost, LightGBM, Random Forest) para enfermedades comunes, y modelos especializados (Prototypical Networks, Siamese Networks, Transfer Learning) para enfermedades huérfanas.
  - **Validación robusta:** K-Fold Cross-Validation, Stratified Sampling, validación temporal.
  - **Métricas médicas ampliadas:** Sensibilidad, Especificidad, PPV, NPV, F1, AUC-ROC con justificación clínica de cada una.

#### Registro de Modelos
- **Versión 1.0:** "Registro de modelos: almacenamiento y versionamiento de modelos validados en un Model Registry."
- **Versión 2.0:** Se especifica MLflow Model Registry con estados del modelo (Staging, Production, Archived), metadata completa (fecha de entrenamiento, métricas, datos de entrenamiento), y trazabilidad completa.

#### Despliegue
- **Versión 1.0:** "Se realiza el despliegue del modelo en entornos reales, garantizando disponibilidad y escalabilidad mediante Docker, Kubernetes y CI/CD."
- **Versión 2.0:** Se detalla:
  - **Estrategia dual completa:** Deployment local con Docker Desktop + UI en localhost + SQLite para logs vs deployment cloud con Kubernetes + auto-scaling + load balancing + API REST centralizada.
  - **Proceso de containerización:** Dockerfile específico, serialización del modelo (pickle/ONNX), health checks.
  - **CI/CD detallado:** Pipeline completo con tests unitarios, linting, security scans, model validation, build de Docker, push a registry, deployment a staging/production.

#### Monitoreo
- **Versión 1.0:** "Se implementa un monitoreo continuo de desempeño, infraestructura, con alertas automáticas ante degradación."
- **Versión 2.0:** Se especifica:
  - **Model monitoring:** Evidently AI para drift detection (data drift y concept drift), A/B testing.
  - **Infrastructure monitoring:** Prometheus + Grafana para métricas (CPU, memoria, latencia), CloudWatch/Azure Monitor para logs.
  - **Alerting:** Sistema de alertas multi-canal (Slack, Email, PagerDuty) con diferentes niveles de severidad.

#### Reentrenamiento
- **Versión 1.0:** "Cuando se detectan cambios en los datos o baja precisión, se activa un proceso de reentrenamiento automático, asegurando mejora continua."
- **Versión 2.0:** Se detalla:
  - **Feedback loop completo:** Captura de predicciones + outcome real, logging de casos fallidos, análisis de feedback.
  - **Trigger automático:** Basado en drift threshold o degradación de métricas.
  - **Pipeline de reentrenamiento:** Airflow DAG o GitHub Action que obtiene datos actualizados, reentrena, evalúa, compara con modelo actual, y despliega si supera métricas.
  - **Aprobación:** Manual o automática según nivel de confianza.

---

### 📈 IMPROVED - Mejoras Sustanciales

#### Interpretabilidad
- **Antes:** Mencionada implícitamente al preferir XGBoost y Random Forest.
- **Ahora:** Dedicada una sección completa a interpretabilidad con SHAP, explicando por qué es crítico en medicina y cómo se implementa para explicar cada predicción.

#### Cumplimiento Regulatorio
- **Antes:** Mencionado HIPAA y GDPR en una línea.
- **Ahora:** Sección detallada sobre seguridad y privacidad, incluyendo encriptación (en tránsito y en reposo), anonimización (k-anonymity), auditoría de accesos, y procedimientos de cumplimiento (audits, derecho al olvido).

#### Escalabilidad
- **Antes:** Mencionada como objetivo general.
- **Ahora:** Estrategias concretas: Kubernetes auto-scaling, caching de predicciones, model serving en GPU (AWS Inferentia, NVIDIA Triton), edge deployment con cuantización para dispositivos móviles.

#### Justificación de Tecnologías
- **Antes:** Tecnologías listadas sin mayor explicación.
- **Ahora:** Cada tecnología viene acompañada de justificación: por qué se eligió, qué problema resuelve, y qué alternativas existen.

#### Reproducibilidad
- **Antes:** No explícitamente mencionada.
- **Ahora:** Garantizada mediante DVC (data versioning), MLflow (experiment tracking), Docker (environment consistency), y Git (code versioning). Cualquier experimento puede reproducirse exactamente.

#### Manejo de Enfermedades Huérfanas
- **Antes:** Mencionado como parte del problema pero sin estrategia clara.
- **Ahora:** Estrategia completa con técnicas especializadas (Few-Shot Learning, Meta-Learning, Transfer Learning, Data Augmentation, SMOTE), frameworks específicos (learn2learn), y justificación de por qué cada técnica aplica.

---

### 🆕 NEW SECTIONS - Secciones Completamente Nuevas

1. **Part 2: Consideraciones Especiales del Problema**
   - Manejo del desbalance de datos
   - Seguridad y privacidad
   - Escalabilidad

2. **Part 3: Escenarios Futuros y Adaptabilidad**
   - Predicciones en tiempo real (<1s)
   - Reentrenamiento con feedback de usuarios
   - Multi-modelo por especialidad
   - Integración con sistemas hospitalarios (HL7 FHIR)

3. **Tecnologías Principales - Stack Completo**
   - Tabla organizada por fase con todas las tecnologías y sus alternativas

4. **Suposiciones Principales**
   - Lista numerada de 8 suposiciones críticas con sus implicaciones

5. **Diagrama del Pipeline**
   - Referencia a diagrama visual (a crear) con todas las etapas y flujos

---

### 🎯 IMPACT - Impacto de los Cambios

#### Claridad y Detalle
- **Antes:** Propuesta de 200-300 palabras, nivel conceptual alto.
- **Ahora:** Propuesta de ~6000 palabras, nivel de especificación técnica suficiente para iniciar implementación.

#### Viabilidad de Implementación
- **Antes:** Roadmap general, equipo necesitaría tomar muchas decisiones técnicas.
- **Ahora:** Blueprint detallado, equipo puede seguir la propuesta como guía de implementación con decisiones técnicas pre-justificadas.

#### Cobertura de MLOps
- **Antes:** Cubría training y deployment básico.
- **Ahora:** Cubre el ciclo completo de MLOps: versionamiento (código, datos, modelos), experiment tracking, CI/CD, monitoring, drift detection, feedback loop, reentrenamiento automático.

#### Consideración de Restricciones Reales
- **Antes:** Mencionaba restricciones regulatorias de forma general.
- **Ahora:** Detalla cómo cumplir con HIPAA/GDPR en cada etapa, desde anonimización de datos hasta auditoría de accesos y derecho al olvido.

#### Adaptabilidad
- **Antes:** Pipeline estático.
- **Ahora:** Pipeline flexible con escenarios futuros contemplados (tiempo real, multi-modelo, integración hospitalaria), permitiendo evolución sin rediseño completo.

---

## Resumen Ejecutivo de Cambios

| Aspecto                     | Versión 1.0                | Versión 2.0                           |
|-----------------------------|----------------------------|---------------------------------------|
| **Longitud**                | ~300 palabras              | ~6000 palabras                        |
| **Nivel de Detalle**        | Conceptual                 | Especificación técnica                |
| **Fases del Pipeline**      | 3 fases generales          | 3 fases con 15+ sub-etapas detalladas |
| **Tecnologías**             | 6 mencionadas              | 30+ tecnologías con justificación     |
| **Versionamiento**          | No especificado            | DVC, Git, MLflow Registry             |
| **Experiment Tracking**     | No especificado            | MLflow completo                       |
| **CI/CD**                   | Mencionado sin detalle     | GitHub Actions pipeline completo      |
| **Monitoring**              | Mencionado sin detalle     | Evidently AI + Prometheus + Grafana   |
| **Interpretabilidad**       | Implícita                  | SHAP con explicaciones detalladas     |
| **Enfermedades Huérfanas**  | Problema identificado      | Estrategia completa (Few-Shot, Meta-Learning) |
| **Deployment**              | Docker + Kubernetes        | Estrategia dual (local offline + cloud online) |
| **Feedback Loop**           | Reentrenamiento automático | Ciclo completo: captura → análisis → trigger → reentrenamiento → validación → deployment |
| **Suposiciones**            | No documentadas            | 8 suposiciones explícitas             |
| **Escenarios Futuros**      | No contemplados            | 4 escenarios con estrategias          |
| **Seguridad/Compliance**    | Mencionado HIPAA/GDPR      | Detalles de encriptación, anonimización, auditoría |

---

## Conclusión

La evolución de la Versión 1.0 a la Versión 2.0 representa un salto cualitativo de una propuesta conceptual a una especificación técnica implementable. Los conocimientos adquiridos durante el curso en MLOps (versionamiento, experiment tracking, CI/CD, monitoring, drift detection, feedback loops) se reflejan en un pipeline robusto, escalable, y alineado con mejores prácticas de la industria.

El pipeline actual no solo resuelve el problema de clasificación de enfermedades, sino que lo hace de forma reproducible, monitoreada, automatizada, y en constante mejora, cumpliendo con restricciones médico-legales y preparado para escalar desde un consultorio local hasta infraestructura hospitalaria cloud.

---

**Autor:** Santiago Prado  
**Fecha del Changelog:** Noviembre 2025  
**Versión Actual del Pipeline:** 2.0

