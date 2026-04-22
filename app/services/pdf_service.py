from pdfminer.high_level import extract_text
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        with io.BytesIO(file_bytes) as pdf_file:
                text = extract_text(pdf_file)
        return text
    except Exception as e:
        raise Exception(f"Error al procesar PDF: {str(e)}")