from fastapi import FastAPI, UploadFile, File
# Importamos FastAPI (framework) y herramientas para manejar archivos

app = FastAPI()
# Creamos la aplicación (es el "servidor")

@app.get("/")
def read_root():
    # Endpoint simple de prueba (cuando entrás a la raíz)
    return {"mensaje": "Hola, tu API funciona"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Endpoint que recibe un archivo
    
    # UploadFile representa el archivo que manda el usuario
    # File(...) indica que el archivo es obligatorio
    
    return {
        "filename": file.filename,        # nombre del archivo
        "content_type": file.content_type # tipo (ej: application/pdf)
    }