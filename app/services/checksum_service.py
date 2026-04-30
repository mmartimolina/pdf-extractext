# Servicio encargado de generar un identificador único del archivo

import hashlib

def calcular_checksum(file_bytes: bytes) -> str:
    """
    Genera un hash único (checksum) del archivo.
    """
    return hashlib.md5(file_bytes).hexdigest()