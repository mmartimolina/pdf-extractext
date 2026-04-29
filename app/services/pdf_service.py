from fastapi import HTTPException
from pdfminer.high_level import extract_text
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extrae el texto de un archivo PDF recibido en formato binario.
    Maneja errores devolviendo una excepción HTTP controlada.
    """

    try:
        with io.BytesIO(file_bytes) as pdf_file:
            text = extract_text(pdf_file)
        return text

    except Exception as e:
        # Se transforma el error en una respuesta HTTP clara para el cliente
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar PDF: {str(e)}"
        )