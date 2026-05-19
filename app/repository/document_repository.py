# Capa de acceso a datos (MongoDB)
# Implementa operaciones CRUD desacopladas del resto de la aplicación


import os
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/pdf_db")

client = MongoClient(MONGO_URI)

# Base de datos
db = client["pdf_db"]

# Colección
collection = db["documents"]
collection.create_index("checksum", unique=True)  # Asegurar que el checksum sea único  


# CREATE
def guardar_documento(documento):

    #Auditoria
    documento["created_at"] = datetime.utcnow()
    documento["updated_at"] = datetime.utcnow() 
    
    #Soft delete
    documento["deleted"] = False    
    documento["deleted_at"] = None

    try:
        return collection.insert_one(documento)
    except DuplicateKeyError:
        return None

# READ (por checksum)
def obtener_por_checksum(checksum: str):
    return collection.find_one({
        "checksum": checksum,
        "deleted": False  # Solo documentos no eliminados
    })


# READ (todos)
def obtener_todos():
    documentos = list(collection.find({
        "deleted": False  # Solo documentos no eliminados
    }))

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

    #Auditoria
    update_fields["updated_at"] = datetime.utcnow()  # Actualizar timestamp de actualización
    resultado = collection.update_one(
        {"checksum": checksum},
        {"deleted": False},  # Asegurar que el documento no esté marcado como eliminado
        {"$set": update_fields}
    )

    if resultado.matched_count == 0:
        return None

    return collection.find_one({
        "checksum": checksum,
        "deleted": False  # Solo documentos no eliminados
    })


# DELETE (por checksum)
def eliminar_documento(checksum: str):
    resultado = collection.update_one(
        {"checksum": checksum,
         "deleted":False},
        {"$set": {
            "deleted": True,
            "deleted_at": datetime.utcnow()  # Marcar fecha de eliminación
        }}
    )   
    return resultado.modified_count > 0     