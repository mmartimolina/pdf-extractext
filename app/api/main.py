# Importamos las herramientas necesarias de FastAPI
from fastapi import FastAPI, UploadFile, File, HTTPException

# Importamos nuestros servicios (lógica de negocio)
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import summarize_text
from app.services.checksum_service import calcular_checksum
from app.repository.document_repository import guardar_documento, obtener_por_checksum

# Creamos la aplicación principal
app = FastAPI()


# Endpoint raíz (opcional, para probar que la API funciona)
@app.get("/")
def read_root():
    return {"mensaje": "Hola, tu API funciona correctamente"}


# Endpoint para subir un archivo PDF
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Este endpoint recibe un archivo PDF, valida su formato y tamaño,
    extrae el texto y devuelve un resumen.
    """

    # Validar que el archivo sea un PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )

    # Leer el archivo en memoria 
    #  No se guarda en disco 
    contenido = await file.read()

    # Validar tamaño  (5MB máximo)  
    if len(contenido) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande (máx 5MB)"
        )

    # Extraer texto usando el service
    # Le pasamos los bytes del archivo (no una ruta)
    texto = extract_text_from_pdf(contenido)

    # Generar resumen 
    resumen = summarize_text(texto)

    # Generar checksum
    checksum = calcular_checksum(contenido)
   
    # Verificar duplicado
    if obtener_por_checksum(checksum):
        raise HTTPException(
            status_code=400,
            detail="El documento ya fue subido anteriormente"
    )

    # Guardar en base de datos
    documento = {
        "filename": file.filename,
        "texto": texto,
        "checksum": checksum
    }

    guardar_documento(documento)
    # Devolver respuesta    
    return {
        "filename": file.filename,          
        "texto_extraido": texto[:500],      
        "resumen": resumen,
        "checksum": checksum
    }
