# Usar imagen base oficial de Python
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="Sistema de Diagnóstico Médico"
LABEL version="1.0.0"
LABEL description="Servicio Docker para diagnóstico médico con ML"

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto 5000
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Healthcheck para verificar que el servicio está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

