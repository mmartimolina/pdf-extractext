from pymongo import MongoClient

# Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017")

# Base de datos
db = client["pdf_db"]

# Colección
collection = db["documents"]


def guardar_documento(documento: dict):
    return collection.insert_one(documento)


def obtener_por_checksum(checksum: str):
    return collection.find_one({"checksum": checksum})


def obtener_todos():
    return list(collection.find())


def eliminar_por_id(id):
    return collection.delete_one({"_id": id})