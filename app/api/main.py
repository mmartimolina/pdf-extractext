# Importamos las herramientas necesarias de FastAPI
from fastapi import FastAPI, UploadFile, File, HTTPException

# Importamos nuestros servicios (lógica de negocio)
from app.services.pdf_service import extract_text_from_pdf
from app.services import ai_service
from app.services.checksum_service import calcular_checksum
from app.models.document_model import UpdateDocumento

# Importamos el repository (CRUD completo)
from app.repository.document_repository import (
    guardar_documento,
    obtener_por_checksum,
    obtener_todos,
    actualizar_documento,
    eliminar_documento
)

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
    contenido = await file.read()

    # Validar tamaño (5MB máximo)
    if len(contenido) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande (máx 5MB)"
        )

    # Extraer texto usando el service
    texto = extract_text_from_pdf(contenido)

    # Generar resumen
    resumen = ai_service.summarize_text(texto)

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


# =========================
# READ → obtener todos
# =========================
@app.get("/documentos")
def listar_documentos():
    documentos = obtener_todos()

    return {
        "total": len(documentos),
        "documentos": documentos
    }


# =========================
# UPDATE → actualizar
# =========================
@app.put("/documentos/{checksum}")
def actualizar_doc(checksum: str, data: UpdateDocumento):
    """
    Actualiza un documento existente identificado por su checksum.
    Se utiliza un modelo Pydantic para validar y tipar los datos de entrada.
    """

    doc_actualizado = actualizar_documento(
        checksum,
        data.filename,
        data.texto
    )

    # Si no se encontró el documento, se devuelve error 404
    if not doc_actualizado:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    return {
        "mensaje": "Documento actualizado",
        "documento": doc_actualizado
    }


# =========================
# DELETE → eliminar
# =========================
@app.delete("/documentos/{checksum}")
def eliminar_doc(checksum: str):

    doc = obtener_por_checksum(checksum)

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    eliminar_documento(checksum)

    return {
        "mensaje": "Documento eliminado correctamente"
    }
@app.get("/documentos/{checksum}")
def obtener_doc(checksum: str):
    """
    Obtiene un documento específico a partir de su checksum.
    """

    doc = obtener_por_checksum(checksum)

    # Validación de existencia
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    # Conversión necesaria para que Mongo sea serializable en JSON
    doc["_id"] = str(doc["_id"])

    return doc