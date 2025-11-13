# Pipeline MLOps - Sistema de Diagnóstico Médico

## Explicación de las Fases

### 1. Fase de Diseño

En esta etapa se definen los requerimientos clínicos, técnicos y regulatorios del sistema. Se establecen las restricciones de privacidad (HIPAA, GDPR), los niveles de servicio (SLA) y los tipos de datos a manejar (estructurados, semi-estructurados y no estructurados). El objetivo es garantizar la seguridad, interpretabilidad y cumplimiento normativo desde la concepción del proyecto.

#### Argumentación de Decisiones de Diseño

**Selección de Modelos Interpretables (XGBoost, Random Forest):**
- **Razón:** En el contexto médico, la interpretabilidad es crítica para la aceptación clínica y el cumplimiento regulatorio. Los modelos de caja negra (como redes neuronales profundas) pueden tener mejor rendimiento, pero no permiten explicar por qué se tomó una decisión diagnóstica.
- **Justificación:** Los médicos necesitan entender el razonamiento del modelo para confiar en sus predicciones. XGBoost y Random Forest proporcionan importancia de características y visualizaciones de árboles de decisión que facilitan la explicación clínica.
- **Caso específico - Enfermedades Huérfanas:** Para enfermedades con pocos datos, estos modelos permiten incorporar conocimiento experto mediante características diseñadas manualmente y pueden funcionar mejor con datasets pequeños que modelos más complejos que requieren grandes volúmenes de datos.

**Estrategia para Datos Escasos (Enfermedades Huérfanas):**
- **Problema:** Las enfermedades raras o huérfanas tienen muy pocos casos documentados, lo que impide entrenar modelos tradicionales que requieren grandes datasets.
- **Solución adoptada:**
  1. **Transfer Learning:** Utilizar modelos pre-entrenados en enfermedades comunes y ajustarlos (fine-tuning) con los pocos datos disponibles de enfermedades huérfanas.
  2. **Data Augmentation:** Generar datos sintéticos mediante técnicas como SMOTE (Synthetic Minority Oversampling Technique) o GANs (Generative Adversarial Networks) específicas para datos médicos, siempre validando con expertos clínicos.
  3. **Few-Shot Learning:** Implementar técnicas de aprendizaje con pocos ejemplos, como prototipos de clases o modelos basados en métricas que aprenden a comparar casos similares.
  4. **Incorporación de Conocimiento Experto:** Diseñar características basadas en literatura médica y conocimiento de expertos, reduciendo la dependencia de datos históricos.
  5. **Ensemble de Modelos Simples:** Combinar múltiples modelos simples (cada uno especializado en un aspecto) que requieren menos datos que un modelo complejo único.

**Justificación de la Arquitectura de Datos:**
- **Múltiples fuentes de datos:** Se integran datos estructurados (signos vitales, laboratorios), semi-estructurados (notas clínicas) y no estructurados (imágenes, texto libre) para capturar la complejidad del diagnóstico médico.
- **Razón:** Un diagnóstico completo requiere información multimodal. Por ejemplo, una fiebre alta (estructurado) combinada con una descripción de síntomas en notas clínicas (no estructurado) proporciona contexto adicional.

---

### 2. Fase de Desarrollo

Se construye la base del pipeline de datos y el modelo de aprendizaje automático. Incluye:
- Ingesta y almacenamiento de datos clínicos desde múltiples fuentes.
- Preprocesamiento: limpieza, normalización y creación de variables relevantes.
- Entrenamiento y validación: uso de modelos interpretables (XGBoost, Random Forest) con métricas clínicas y validación cruzada.
- Registro de modelos: almacenamiento y versionamiento de modelos validados en un Model Registry.

El objetivo es generar un modelo confiable, reproducible y clínicamente verificable.

#### Argumentación de Decisiones de Desarrollo

**Preprocesamiento Específico para Casos con Pocos Datos:**
- **Normalización robusta:** Para enfermedades huérfanas, se utiliza normalización basada en percentiles en lugar de media/desviación estándar, ya que los outliers son comunes y valiosos en datasets pequeños.
- **Manejo de valores faltantes:** En lugar de eliminar casos con datos incompletos (crítico cuando hay pocos), se implementa imputación múltiple con validación cruzada, preservando la incertidumbre en los datos.

**Métricas Clínicas vs. Métricas Tradicionales:**
- **Razón:** La precisión general puede ser engañosa en medicina. Un modelo con 95% de precisión que falla en detectar enfermedades graves es inaceptable.
- **Métricas adoptadas:**
  - **Sensibilidad (Recall) para clases críticas:** Priorizar la detección de enfermedades agudas, incluso a costa de falsos positivos.
  - **Especificidad:** Reducir falsos negativos que pueden tener consecuencias graves.
  - **F1-Score por clase:** Balance entre precisión y recall para cada categoría diagnóstica.
  - **AUC-ROC multiclase:** Evaluar la capacidad del modelo de distinguir entre todas las clases, especialmente importante cuando hay desbalance de clases.

**Validación Cruzada Estratificada:**
- **Justificación:** En datasets pequeños o desbalanceados (como enfermedades huérfanas), la validación cruzada estratificada asegura que cada fold mantenga la proporción de clases, proporcionando estimaciones más confiables del rendimiento.

**Model Registry y Versionamiento:**
- **Razón:** En medicina, la trazabilidad es esencial. Cada modelo debe estar versionado con sus hiperparámetros, datos de entrenamiento y métricas de validación para cumplir con regulaciones y permitir auditorías.

---

### 3. Fase de Producción

Se realiza el despliegue del modelo en entornos reales, garantizando disponibilidad y escalabilidad mediante Docker, Kubernetes y CI/CD. El modelo se ofrece vía API REST para integración con sistemas hospitalarios. Se implementa un monitoreo continuo de desempeño, infraestructura, con alertas automáticas ante degradación. Cuando se detectan cambios en los datos o baja precisión, se activa un proceso de reentrenamiento automático, asegurando mejora continua.

#### Argumentación de Decisiones de Producción

**Containerización con Docker:**
- **Razón:** Los sistemas hospitalarios tienen entornos heterogéneos. Docker garantiza que el modelo funcione de manera idéntica en desarrollo, pruebas y producción, eliminando problemas de "funciona en mi máquina".
- **Beneficio adicional:** Facilita el despliegue en diferentes hospitales sin modificar la infraestructura existente.

**API REST para Integración:**
- **Justificación:** Los sistemas hospitalarios (HIS, EMR) requieren integración mediante interfaces estándar. REST es ampliamente soportado y permite integración sin modificar sistemas legacy.
- **Latencia:** Para diagnósticos en tiempo real, REST proporciona respuestas rápidas (< 100ms) comparado con procesamiento batch.

**Monitoreo Continuo y Reentrenamiento Automático:**
- **Razón crítica:** Los modelos médicos sufren "data drift" - los patrones de enfermedades cambian (nuevas cepas, cambios demográficos, estacionalidad). Un modelo estático se degrada con el tiempo.
- **Estrategia de detección:**
  1. **Monitoreo de distribución de datos:** Detectar cambios estadísticos en las características de entrada (ej: aumento de temperatura promedio en pacientes).
  2. **Monitoreo de rendimiento:** Alertas cuando la precisión cae por debajo de umbrales predefinidos.
  3. **Análisis de concept drift:** Detectar cuando la relación entre características y diagnóstico cambia (ej: nueva variante de virus con síntomas diferentes).

**Reentrenamiento Automático con Validación Humana:**
- **Proceso:** Cuando se detecta degradación, se activa reentrenamiento, pero **siempre requiere validación de expertos clínicos** antes del despliegue en producción.
- **Justificación:** En medicina, un modelo mal entrenado puede tener consecuencias graves. La automatización acelera el proceso, pero la validación humana es un checkpoint obligatorio.

**Escalabilidad con Kubernetes:**
- **Razón:** Los sistemas hospitalarios requieren alta disponibilidad (99.9% uptime). Kubernetes permite auto-escalado según demanda y recuperación automática ante fallos, crítico para sistemas de diagnóstico que no pueden estar caídos.

---

## Link al Diagrama Visual

[Diagrama Pipeline MLOps en Miro](https://miro.com/welcomeonboard/bEhRTndJOXJUR1BsR0ZkblpqM0IrQklqSVZJUlE5bE1OSng0WHpkRDZ6bW1NVGV6czNKU1VJR2FoRHE3T3cvaFBid1dMN0ZHU0ZhVWhCKzAyMUwxdm0wMXV0WEMxSDFNNnYwMW42S1NEekpkVExTZ1NYcnNpZG1hMi9QNXNYRyt0R2lncW1vRmFBVnlLcVJzTmdFdlNRPT0hdjE=?share_link_id=807529502980)
