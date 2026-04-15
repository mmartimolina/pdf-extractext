from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path: str) -> str:
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        raise Exception(f"Error al procesar PDF: {str(e)}")