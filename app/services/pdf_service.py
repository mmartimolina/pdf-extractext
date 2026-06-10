# Servicio responsable de la extracción de texto desde PDFs

from fastapi import HTTPException
from pdfminer.high_level import extract_text
import io
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extrae el texto de un archivo PDF recibido en formato binario.
    Maneja errores devolviendo una excepción HTTP controlada.
    """
    try:
        logger.info("Iniciando extracción de texto PDF")

        with io.BytesIO(file_bytes) as pdf_file:
            text = extract_text(pdf_file)

        logger.info("Extracción completada correctamente")

        return text

    except Exception as e:

        logger.error(
            f"Error durante la extracción del PDF: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar PDF: {str(e)}"
        )
    
    