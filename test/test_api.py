from app.repository.document_repository import collection
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api.main import app
import os

client = TestClient(app)

# Ruta base del archivo actual (para manejar paths correctamente)
BASE_DIR = os.path.dirname(__file__)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hola, tu API funciona correctamente"}

def test_listar_documentos():
    response = client.get("/documentos")

    assert response.status_code == 200
    assert "documentos" in response.json()


@patch("app.services.ai_service.summarize_text")
def test_upload_pdf(mock_summary):
    mock_summary.return_value = "Resumen de prueba"

    #  limpiar base antes del test
    collection.delete_many({})

    file_path = os.path.join(BASE_DIR, "sample.pdf")

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload-pdf",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200

    data = response.json()

    assert "checksum" in data
    assert "resumen" in data
    assert "filename" in data