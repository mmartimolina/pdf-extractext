# 📄 PDF ExtractExt API

## 📖 Descripción

**PDF ExtractExt** es una API REST desarrollada con **FastAPI** que permite procesar documentos PDF de forma automática.

La aplicación recibe archivos PDF, extrae su contenido textual, genera automáticamente un resumen mediante un  servicio de Inteligencia Artificial y almacena la información en una base de datos MongoDB para su posterior consulta mediante operaciones CRUD.

El proyecto fue desarrollado aplicando buenas prácticas de desarrollo, contenedores Docker, pruebas automatizadas y una arquitectura organizada por capas, facilitando su mantenimiento y escalabilidad.

## ✨ Características

| Funcionalidad | Descripción | Estado |
|--------------|-------------|:------:|
| 📄 Extracción de texto | Obtiene el contenido textual de archivos PDF | ✅ |
| 🤖 Resumen con IA | Genera un resumen automático del contenido extraído | ✅ |
| 🗄️ Persistencia | Almacena documentos y resúmenes en MongoDB | ✅ |
| 🔄 Operaciones CRUD | Permite crear, consultar, actualizar y eliminar documentos | ✅ |
| 🔐 Validaciones | Verifica tipo de archivo, tamaño y documentos duplicados | ✅ |
| 🧾 Checksum | Genera un identificador único para evitar duplicados | ✅ |
| 🗑️ Soft Delete | Elimina documentos de forma lógica preservando la información | ✅ |
| 🐳 Docker | Despliegue mediante contenedores Docker y Docker Compose | ✅ |
| 📖 Swagger UI | Documentación interactiva de la API | ✅ |
| 🧪 Testing | Pruebas automatizadas con Pytest | ✅ |

## 🛠 Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|------------|-------------------------|
| Python | Lenguaje principal de desarrollo |
| FastAPI | Desarrollo de la API REST |
| MongoDB | Base de datos NoSQL para persistencia |
| Docker | Contenerización de la aplicación |
| Docker Compose | Orquestación de servicios |
| pdfminer.six | Extracción de texto desde archivos PDF |
| Requests | Comunicación con el servicio de IA |
| Pytest | Pruebas automatizadas |
| Git & GitHub | Control de versiones |

## 🏛 Arquitectura

El proyecto sigue una arquitectura en capas que permite separar responsabilidades y facilitar el mantenimiento, escalabilidad y la reutilización del código.

```text
                Cliente
                   │
                   ▼
            FastAPI (API REST)
                   │
                   ▼
          Servicios de Negocio
                   │
                   ▼
       Repositorio (MongoDB)
                   │
                   ▼
              Base de Datos
```

### Responsabilidades de cada capa

| Capa | Responsabilidad |
|------|-----------------|
| API | Recibe las solicitudes HTTP y devuelve las respuestas al cliente. |
| Servicios | Contiene la lógica de negocio, procesamiento de PDFs y generación de resúmenes. |
| Repositorio | Gestiona el acceso a la base de datos MongoDB. |
| Base de datos | Almacena los documentos, resúmenes y metadatos. |

## 📂 Estructura del proyecto
```text
pdf-extractext/
│
├── app/
│   ├── api/
│   │   └── main.py
│   ├── models/
│   ├── repository/
│   └── services/
│
├── documents/
│   └── diagrams/
│
├── test/
│
├── scripts/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env.example
```

## 🔄 Flujo del sistema

El procesamiento de un documento sigue el siguiente flujo:

```text
Usuario

   │

   ▼

Sube un archivo PDF

   │

   ▼

Validación del archivo

   │

   ▼

Extracción del texto

   │

   ▼

Generación del resumen mediante IA

   │

   ▼

Cálculo del checksum

   │

   ▼

Almacenamiento en MongoDB

   │

   ▼

Respuesta JSON al cliente
```

## ⚙ Instalación

### Requisitos previos

Antes de ejecutar el proyecto es necesario contar con:

- Git
- Docker y Docker Compose
- Python 3.14 (solo para ejecución local)

> **Nota:** También es posible ejecutar la aplicación localmente utilizando Python y las dependencias del proyecto, aunque se recomienda Docker para simplificar la configuración.

### 1. Clonar el repositorio

```bash
git clone https://github.com/mmartimolina/pdf-extractext.git
cd pdf-extractext
```

### 2. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto utilizando como referencia el archivo `.env.example`.

Ejemplo:

```env
API_KEY=tu_api_key
MONGO_URI=mongodb://mongo:27017/pdf_db
```

### 3. Ejecutar con Docker

```bash
docker compose up --build
```

### 4. Acceder a la documentación

Una vez iniciado el proyecto:

```text
http://localhost:8000/docs
```

Desde Swagger UI es posible probar todos los endpoints de forma interactiva.


## 🌍 Variables de entorno

| Variable | Descripción |
|----------|-------------|
| API_KEY | Clave utilizada para consumir el servicio de Inteligencia Artificial. |
| MONGO_URI | Cadena de conexión a MongoDB. |

Ejemplo:

```env
API_KEY=tu_api_key
MONGO_URI=mongodb://mongo:27017/pdf_db
```

## 🐳 Docker

El proyecto se encuentra completamente dockerizado mediante **Docker** y **Docker Compose**, facilitando su despliegue en cualquier entorno.

### Comandos principales

```bash
# Construir e iniciar los servicios
docker compose up --build

# Detener los servicios
docker compose down

# Ver los logs
docker compose logs

# Reiniciar los servicios
docker compose restart

# Detener los servicios sin eliminarlos
docker compose stop
```

## 📡 Endpoints

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| POST | `/upload-pdf` | Sube un archivo PDF, extrae el texto y genera un resumen. |
| GET | `/documentos` | Obtiene la lista de documentos almacenados. |
| GET | `/documentos/{checksum}` | Obtiene un documento mediante su checksum. |
| PUT | `/documentos/{checksum}` | Actualiza la información de un documento. |
| DELETE | `/documentos/{checksum}` | Realiza un Soft Delete del documento, marcándolo como eliminado sin borrar físicamente la información. |
| GET | `/health` | Verifica el estado de la API y la conexión con MongoDB. |

## 📌 Ejemplos de solicitudes y respuestas de endpoints

A continuación se muestran ejemplos de uso de los principales endpoints disponibles en la API.

---

## 📄 POST `/upload-pdf`

Permite subir un archivo PDF, extraer su contenido, generar un resumen mediante IA y almacenarlo en MongoDB.

### Solicitud

```http
POST /upload-pdf
Content-Type: multipart/form-data
```

Body:

```text
file: documento.pdf
```

### Respuesta exitosa `200 OK`

```json
{
  "filename": "documento.pdf",
  "texto_extraido": "Contenido extraído del PDF...",
  "resumen": "Resumen generado mediante Inteligencia Artificial...",
  "checksum": "a83f91d8c..."
}
```

### Respuestas de error

Archivo con formato incorrecto:

```json
{
  "detail": "El archivo debe ser un PDF"
}
```

Archivo demasiado grande:

```json
{
  "detail": "El archivo es demasiado grande (máx 5MB)"
}
```

Documento duplicado:

```json
{
  "detail": "El documento ya fue subido anteriormente"
}
```

---

## 📚 GET `/documentos`

Obtiene todos los documentos almacenados en la base de datos.

### Solicitud

```http
GET /documentos
```

### Respuesta exitosa `200 OK`

```json
{
  "total": 1,
  "documentos": [
    {
      "filename": "documento.pdf",
      "texto": "Contenido extraído del PDF...",
      "resumen": "Resumen generado mediante Inteligencia Artificial...",
      "checksum": "a83f91d8c..."
    }
  ]
}
```

---

## 🔎 GET `/documentos/{checksum}`

Obtiene un documento específico utilizando su identificador único.

### Solicitud

```http
GET /documentos/a83f91d8c
```

### Respuesta exitosa `200 OK`

```json
{
  "filename": "documento.pdf",
  "texto": "Contenido extraído del PDF...",
  "resumen": "Resumen generado mediante Inteligencia Artificial...",
  "checksum": "a83f91d8c"
}
```

### Documento inexistente

```json
{
  "detail": "Documento no encontrado"
}
```

---

## ✏️ PUT `/documentos/{checksum}`

Actualiza la información de un documento existente.

### Solicitud

```http
PUT /documentos/a83f91d8c
Content-Type: application/json
```

Body:

```json
{
  "filename": "nuevo_nombre.pdf",
  "texto": "Nuevo contenido del documento"
}
```

### Respuesta exitosa `200 OK`

```json
{
  "mensaje": "Documento actualizado",
  "documento": {
    "filename": "nuevo_nombre.pdf",
    "texto": "Nuevo contenido del documento"
  }
}
```

### Documento inexistente

```json
{
  "detail": "Documento no encontrado"
}
```

---

## 🗑️ DELETE `/documentos/{checksum}`

Realiza un Soft Delete del documento identificado mediante checksum.

### Solicitud

```http
DELETE /documentos/a83f91d8c
```

### Respuesta exitosa `200 OK`

```json
{
  "mensaje": "Documento eliminado correctamente"
}
```

### Documento inexistente

```json
{
  "detail": "Documento no encontrado"
}
```

---

## ❤️ GET `/health`

Verifica el estado de la aplicación y la conexión con MongoDB.

### Solicitud

```http
GET /health
```

### Respuesta exitosa `200 OK`

```json
{
  "application": "OK,Funciona correctamente",
  "database": "OK,Conexión exitosa",
  "timezone": "America/Argentina/Mendoza"
}
```

## 🧪 Testing

El proyecto cuenta con pruebas automatizadas desarrolladas con **Pytest**, permitiendo verificar el correcto funcionamiento de la API y sus principales funcionalidades.

Para ejecutar las pruebas:

```bash
pytest -v
```

## 📊 Diagramas UML

La documentación técnica incluye diagramas UML que describen la arquitectura y el comportamiento del sistema.

Se encuentran disponibles en:

```text
documents/diagrams/
```
Los diagramas incluyen:

- Diagrama de clases.
- Diagrama de secuencia.

## 📚 Principios aplicados

Durante el desarrollo del proyecto se aplicaron distintos principios de ingeniería de software con el objetivo de mejorar la calidad y mantenibilidad del código.

| Principio | Aplicación |
|-----------|------------|
| DRY | Se evitó la duplicación de lógica reutilizando servicios y repositorios. |
| KISS | Se priorizó una solución simple y fácil de mantener. |
| SOLID | Separación de responsabilidades mediante una arquitectura en capas. |
| YAGNI | Se implementaron únicamente las funcionalidades requeridas por el proyecto. |

## 👥 Integrantes

| Integrante | Legajo |
|------------|:------:|
| Martina Abril Molina | 10872 |
| Ana Valentina Astudillo |  |

## 📄 Licencia


Este proyecto fue desarrollado con fines académicos para la asignatura **Desarrollo de Software** de la **Universidad Tecnológica Nacional - Facultad Regional San Rafael (UTN FRSR)**.




