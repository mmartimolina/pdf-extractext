# PDF Extract & Summarize API

API desarrollada con FastAPI que permite:

* Subir archivos PDF
* Extraer su contenido
* Generar un resumen usando IA
* Almacenar documentos en MongoDB
* Gestionar documentos (CRUD completo)

---

## Tecnologías utilizadas

* Python 3.13
* FastAPI
* MongoDB
* pdfminer
* NVIDIA AI (Llama 3.1)
* Pytest (testing)

---

## Arquitectura

El proyecto sigue una estructura por capas:

* **api/** → endpoints (interfaz con el cliente)
* **services/** → lógica de negocio
* **repository/** → acceso a datos (MongoDB)
* **models/** → validación y tipado (Pydantic)
* **test/** → pruebas automatizadas

---

##  Instalación

1. Clonar el repositorio:

```bash
git clone <repo-url>
cd pdf-extractext
```

2. Crear entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear archivo `.env` en la raíz:

```env
API_KEY=tu_api_key_aqui
```

5. Ejecutar MongoDB (local)

---

##  Ejecución

```bash
uvicorn app.api.main:app --reload
```

Acceder a la documentación automática:
👉 http://127.0.0.1:8000/docs

---

##  Endpoints principales

### Subir PDF

```
POST /upload-pdf
```

* Valida formato y tamaño
* Extrae texto
* Genera resumen
* Evita duplicados mediante checksum

---

###  Obtener todos los documentos

```
GET /documentos
```

---

###  Obtener documento por checksum

```
GET /documentos/{checksum}
```

---

###  Actualizar documento

```
PUT /documentos/{checksum}
```

---

###  Eliminar documento

```
DELETE /documentos/{checksum}
```

---

##  Testing

Ejecutar:

```bash
pytest -v
```

✔ Tests rápidos
✔ Mock de IA aplicado
✔ Independientes de servicios externos

---

## Decisiones técnicas

* Uso de **checksum (MD5)** para evitar duplicados
* Separación de capas siguiendo principios **SOLID**
* Uso de **Pydantic** para validación de datos
* Mocking en tests para evitar dependencia de APIs externas

---

##  Licencia

MIT License

---

##  Integrantes

* Astudillo, Ana Valentina
* Molina, Martina Abril
