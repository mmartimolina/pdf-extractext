# FastAPI se utiliza como framework para exponer la API REST
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import logging

# Servicios: encapsulan la lógica de negocio
from app.services.pdf_service import extract_text_from_pdf
from app.services import ai_service
from app.services.checksum_service import calcular_checksum

# Modelos: validación y tipado de datos (Pydantic)
from app.models.document_model import UpdateDocumento
from app.models.document_model import DocumentoResponse

# Importamos el repository (CRUD completo)
from app.repository.document_repository import (
    guardar_documento,
    obtener_por_checksum,
    obtener_todos,
    actualizar_documento,
    eliminar_documento
)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Creamos la aplicación principal
app = FastAPI()


# Endpoint raíz
@app.get("/")
def read_root():
    logger.info("Endpoint raíz consultado")

    return {
        "mensaje": "Hola, tu API funciona correctamente"
    }


# CREATE → Subir PDF

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Este endpoint recibe un archivo PDF, valida su formato y tamaño,
    extrae el texto y devuelve un resumen.
    """

    logger.info(f"PDF recibido: {file.filename}")

    # Validar que el archivo sea un PDF
    if file.content_type != "application/pdf":
        logger.warning(
            f"Archivo rechazado por formato inválido: {file.filename}"
        )

        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )

    # Leer el archivo en memoria
    contenido = await file.read()

    # Validar tamaño (5MB máximo)
    if len(contenido) > 5 * 1024 * 1024:

        logger.warning(
            f"Archivo demasiado grande: {file.filename}"
        )

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

        logger.warning(
            f"Documento duplicado detectado: {file.filename}"
        )

        raise HTTPException(
            status_code=400,
            detail="El documento ya fue subido anteriormente"
        )

    # Guardar en base de datos
    documento = {
        "filename": file.filename,
        "texto": texto,
        "resumen": resumen,
        "checksum": checksum
    }

    guardar_documento(documento)

    logger.info(
        f"Documento almacenado correctamente: {checksum}"
    )

    # Devolver respuesta
    return {
        "filename": file.filename,
        "texto_extraido": texto[:500],
        "resumen": resumen,
        "checksum": checksum
    }


# READ → obtener todos

@app.get("/documentos")
def listar_documentos():

    logger.info("Consulta de listado de documentos")

    documentos = obtener_todos()

    return {
        "total": len(documentos),
        "documentos": [
            {
                "filename": doc["filename"],
                "texto": doc["texto"][:200],
                "resumen": doc.get("resumen"),
                "checksum": doc["checksum"]
            }
            for doc in documentos
        ]
    }


# UPDATE → actualizar

@app.put("/documentos/{checksum}")
def actualizar_doc(checksum: str, data: UpdateDocumento):
    """
    Actualiza un documento existente identificado por su checksum.
    """

    doc_actualizado = actualizar_documento(
        checksum,
        data.filename,
        data.texto
    )

    if not doc_actualizado:

        logger.warning(
            f"Intento de actualización sobre documento inexistente: {checksum}"
        )

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    logger.info(
        f"Documento actualizado: {checksum}"
    )

    return {
        "mensaje": "Documento actualizado",
        "documento": doc_actualizado
    }


# DELETE → eliminar

@app.delete("/documentos/{checksum}")
def eliminar_doc(checksum: str):

    doc = obtener_por_checksum(checksum)

    if not doc:

        logger.warning(
            f"Intento de eliminación sobre documento inexistente: {checksum}"
        )

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    eliminar_documento(checksum)

    logger.info(
        f"Documento eliminado: {checksum}"
    )

    return {
        "mensaje": "Documento eliminado correctamente"
    }


# READ → obtener uno

@app.get("/documentos/{checksum}")
def obtener_doc(checksum: str):

    doc = obtener_por_checksum(checksum)

    if not doc:

        logger.warning(
            f"Documento no encontrado: {checksum}"
        )

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    logger.info(
        f"Consulta de documento: {checksum}"
    )

    return {
        "filename": doc["filename"],
        "texto": doc["texto"][:500],
        "resumen": doc.get("resumen"),
        "checksum": doc["checksum"]
    }


# HEALTH CHECK

@app.get("/health")
def health():

    logger.info("Health check ejecutado")

    try:
        from app.repository.document_repository import collection

        collection.find_one()

        return {
            "application": "OK,Funciona correctamente",
            "database": "OK,Conexión exitosa",
            "timezone": "America/Argentina/Mendoza"
        }

    except Exception as e:

        logger.error(
            f"Error en health check: {str(e)}"
        )

        return {
            "application": "OK,Funciona correctamente",
            "database": "ERROR",
            "timezone": "America/Argentina/Mendoza",
            "detail": str(e)
        }