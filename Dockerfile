# Imagen base
FROM python:3.14-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Argentina/Mendoza

# Dependencias del sistema
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no root
RUN useradd \
    --create-home \
    --home-dir /home/appuser \
    appuser

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Asignar permisos al usuario de la aplicación
RUN chown -R appuser:appuser /app

# Ejecutar como usuario no privilegiado
USER appuser

# Puerto de FastAPI
EXPOSE 8000

# Iniciar aplicación
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]