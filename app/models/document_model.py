from pydantic import BaseModel
from typing import Optional


class Documento(BaseModel):
    # Representa la estructura completa de un documento en el sistema
    filename: str
    texto: str
    checksum: str


class UpdateDocumento(BaseModel):
    # Modelo para actualizaciones parciales (PUT)
    # Todos los campos son opcionales porque el usuario puede modificar solo uno
    filename: Optional[str] = None
    texto: Optional[str] = None

class DocumentoResponse(BaseModel):
    filename: str
    texto: str
    resumen: str | None = None
    checksum: str