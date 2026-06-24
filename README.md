# 📄 PDF Extract 

---

##  Introducción

Este proyecto fue diseñado para automatizar la extracción de texto desde documentos PDF. El propósito principal es optimizar el manejo de información digital, eliminando la necesidad de transcribir contenidos de forma manual y permitiendo que el procesamiento de archivos sea mucho más ágil y sencillo.

---

##  Objetivos

* Automatizar la extracción de texto desde PDFs
* Facilitar el procesamiento de información digital
* Permitir el uso del contenido para análisis, resúmenes o almacenamiento

---

##  Funcionalidades principales

* Extracción automática de texto desde archivos PDF
* Optimización de tiempos de procesamiento
* Preparación de datos para uso en sistemas o modelos de IA

---

##  Arquitectura del sistema

* **Interfaz:** recibe el archivo PDF
* **Procesamiento:** extrae y analiza el contenido
* **Almacenamiento:** guarda la información en base de datos

---

##  Propietarias

Martina Abril Molina
Ana Valentina Astudillo

---

## 🔗 Repositorio

https://github.com/mmartimolina/pdf-extractext

---

##  Descripción técnica

API desarrollada con FastAPI que permite:

* Subir archivos PDF
* Extraer el contenido del documento
* Generar un resumen automático utilizando inteligencia artificial
* Almacenar la información en una base de datos MongoDB
* Gestionar los documentos mediante operaciones CRUD

---

##  Tecnologías utilizadas

* Python
* FastAPI
* MongoDB
* Docker
* Pytest

---

##  Requisitos

* Docker instalado
* Git instalado

---

##  CÓMO EJECUTAR EL PROYECTO

### 1. Clonar el repositorio

```bash
git clone https://github.com/mmartimolina/pdf-extractext.git
cd pdf-extractext
```

---

### 2. Crear archivo `.env`

En la raíz del proyecto crear un archivo `.env` con el siguiente contenido:

```env
API_KEY=tu_api_key
MONGO_URI=mongodb://mongo:27017/pdf_db
```

---

### 3. Ejecutar con Docker

```bash
docker-compose up --build
```

---

### 4. Acceder a la API

Una vez iniciado, ingresar a:

 http://localhost:8000/docs

Desde allí se pueden probar todos los endpoints.

---

##  Endpoints principales

* `POST /upload-pdf` → Subir archivo PDF
* `GET /documentos` → Listar documentos
* `GET /documentos/{checksum}` → Obtener documento
* `PUT /documentos/{checksum}` → Actualizar documento
* `DELETE /documentos/{checksum}` → Eliminar documento
* `GET /health` → Estado del sistema

---

##  Tests

Para ejecutar los tests:

```bash
pytest -v
```

---

## Características destacadas

* Validación de archivos (tipo y tamaño)
* Generación de checksum para evitar duplicados
* Integración con API de IA (resumen automático)
* Persistencia en base de datos NoSQL
* Dockerización completa del sistema
* Tests automatizados
----
## Diagramas UML

Los diagramas del sistema se encuentran en:

docs/diagrams/
