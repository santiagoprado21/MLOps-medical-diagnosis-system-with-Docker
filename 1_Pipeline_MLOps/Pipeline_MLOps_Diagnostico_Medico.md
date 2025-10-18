Explicacion de las fases:

1. Fase de Diseño
En esta etapa se definen los requerimientos clínicos, técnicos y regulatorios del sistema.Se establecen las restricciones de privacidad (HIPAA, GDPR), los niveles de servicio (SLA) y los tipos de datos a manejar (estructurados, semi-estructurados y no estructurados). El objetivo es garantizar la seguridad, interpretabilidad y cumplimiento normativo desde la concepción del proyecto.

2. Fase de Desarrollo
Se construye la base del pipeline de datos y el modelo de aprendizaje automático. Incluye:
Ingesta y almacenamiento de datos clínicos desde múltiples fuentes.
Preprocesamiento: limpieza, normalización y creación de variables relevantes.
Entrenamiento y validación: uso de modelos interpretables (XGBoost, Random Forest) con métricas clínicas y validación cruzada.
Registro de modelos: almacenamiento y versionamiento de modelos validados en un Model Registry.
El objetivo es generar un modelo confiable, reproducible y clínicamente verificable.

3. Fase de Producción
Se realiza el despliegue del modelo en entornos reales, garantizando disponibilidad y escalabilidad mediante Docker, Kubernetes y CI/CD. El modelo se ofrece vía API REST para integración con sistemas hospitalarios. Se implementa un monitoreo continuo de desempeño, infraestructura, con alertas automáticas ante degradación. Cuando se detectan cambios en los datos o baja precisión, se activa un proceso de reentrenamiento automático, asegurando mejora continua.

Link Canva:
https://miro.com/welcomeonboard/bEhRTndJOXJUR1BsR0ZkblpqM0IrQklqSVZJUlE5bE1OSng0WHpkRDZ6bW1NVGV6czNKU1VJR2FoRHE3T3cvaFBid1dMN0ZHU0ZhVWhCKzAyMUwxdm0wMXV0WEMxSDFNNnYwMW42S1NEekpkVExTZ1NYcnNpZG1hMi9QNXNYRyt0R2lncW1vRmFBVnlLcVJzTmdFdlNRPT0hdjE=?share_link_id=807529502980
