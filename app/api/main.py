import os
# os → permite trabajar con el sistema de archivos (crear carpetas, rutas, etc.)

from fastapi import FastAPI, UploadFile, File, HTTPException
# FastAPI → framework para crear la API
# UploadFile → representa el archivo que sube el usuario
# File → indica que el parámetro es un archivo
# HTTPException → permite devolver errores controlados

from app.services.pdf_service import extract_text_from_pdf
# Importamos el servicio que se encarga de extraer el texto del PDF

app = FastAPI()
# Creamos la aplicación principal (servidor)

UPLOAD_DIR = "uploads"
# Definimos la carpeta donde se guardarán los archivos subidos

os.makedirs(UPLOAD_DIR, exist_ok=True)
# Creamos la carpeta "uploads" si no existe
# exist_ok=True evita errores si ya está creada

@app.post("/upload-pdf")
# Definimos un endpoint POST para subir archivos PDF

async def upload_pdf(file: UploadFile = File(...)):
    # file → archivo enviado por el usuario
    # File(...) → indica que es obligatorio

    # Validamos que el archivo sea un PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )

    # Construimos la ruta donde se guardará el archivo
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Guardamos el archivo en el servidor
    with open(file_path, "wb") as buffer:
        # "wb" → write binary (necesario para archivos)
        buffer.write(await file.read())

    # Llamamos al servicio para extraer el texto del PDF
    texto = extract_text_from_pdf(file_path)

    # Devolvemos una respuesta al cliente
    return {
        "filename": file.filename,           # nombre del archivo
        "texto_extraido": texto[:500]        # mostramos solo los primeros 500 caracteres
    }