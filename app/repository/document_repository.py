from pymongo import MongoClient
from bson import ObjectId

# Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017")

# Base de datos
db = client["pdf_db"]

# Colección
collection = db["documents"]


# CREATE
def guardar_documento(documento: dict):
    return collection.insert_one(documento)


# READ (por checksum)
def obtener_por_checksum(checksum: str):
    return collection.find_one({"checksum": checksum})


# READ (todos)
def obtener_todos():
    documentos = list(collection.find())

    # Convertir ObjectId a string para evitar errores JSON
    for doc in documentos:
        doc["_id"] = str(doc["_id"])

    return documentos


# UPDATE
def actualizar_documento(checksum: str, nuevo_nombre=None, nuevo_texto=None):

    update_fields = {}

    if nuevo_nombre:
        update_fields["filename"] = nuevo_nombre

    if nuevo_texto:
        update_fields["texto"] = nuevo_texto

    if not update_fields:
        return None

    resultado = collection.update_one(
        {"checksum": checksum},
        {"$set": update_fields}
    )

    if resultado.matched_count == 0:
        return None

    return collection.find_one({"checksum": checksum})


# DELETE (por checksum)
def eliminar_documento(checksum: str):

    resultado = collection.delete_one({"checksum": checksum})

    return resultado.deleted_count > 0