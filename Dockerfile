FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 8000

# Comando para correr la API
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]