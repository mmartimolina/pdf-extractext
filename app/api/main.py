from fastapi import FastAPI, UploadFile, File
# Importamos FastAPI (framework) y herramientas para manejar archivos

app = FastAPI()
# Creamos la aplicación (es el "servidor")

@app.get("/")
def read_root():
    # Endpoint simple de prueba (cuando entrás a la raíz)
    return {"mensaje": "Hola, tu API funciona"}
from fastapi import FastAPI, UploadFile, File, HTTPException
# Importamos:
# - FastAPI → para crear la API
# - UploadFile y File → para recibir archivos
# - HTTPException → para lanzar errores controlados

app = FastAPI()
# Creamos la aplicación

@app.get("/")
def read_root():
    # Endpoint de prueba
    return {"mensaje": "Hola, tu API funciona"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    
    
    # file: UploadFile → representa el archivo que sube el usuario
    # File(...) → indica que es obligatorio
    
  
    # Verificamos el tipo de archivo
    if file.content_type != "application/pdf":
        
        
        raise HTTPException(
            status_code=400,  
            detail="El archivo debe ser un PDF"  
        )
    
   
    return {
        "filename": file.filename,        
        "content_type": file.content_type 
    }