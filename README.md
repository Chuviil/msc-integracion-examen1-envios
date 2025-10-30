# Examen 1 – Envios

Servicio simple de gestión de envíos que expone una API REST en Python y utiliza Apache Camel (Java) para transformar un CSV (`envios.csv`) a JSON (`src/data/envios.json`).

Puedes ejecutarlo de dos maneras:

- Opción 1: `src/api/app.py` si quieres correr Apache Camel manualmente para generar el JSON.
- Opción 2: `src/api/full.py` si prefieres que el servicio lance el `.jar` de Camel y se encargue de todo automáticamente.

## Requisitos

- Python 3.14.0
- pip (administrador de paquetes de Python)
- Java 17 (requerido solo si vas a usar `full.py` o ejecutar Camel manualmente)
- Maven 3.8+ (para construir el `.jar` de Apache Camel)

## Instalación (Windows – cmd.exe)

1) Crear y activar un entorno virtual (opcional pero recomendado):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

2) Instalar dependencias de Python:

```cmd
pip install -r requirements.txt
```

## Datos de entrada/salida

- Entrada: `envios.csv` en la raíz del repositorio.
- Salida: `src/data/envios.json` (generado por Apache Camel).

El API lee y persiste datos en `src/data/envios.json`.

## Cómo ejecutar

Tienes dos opciones. En ambas, el servicio por defecto escucha en `0.0.0.0:5000`. Puedes cambiar host/puerto con variables de entorno `HOST` y `PORT`.

### Opción 1: API simple (Camel manual) – `app.py`

1) Genera el JSON con Apache Camel (Java):

```cmd
cd src\file-transfer
mvn -q -DskipTests package
java -jar target\file-transfer-1.0-SNAPSHOT.jar
```

Esto leerá `envios.csv` (en la raíz del repo) y creará `src/data/envios.json`.

2) Inicia el API (desde la raíz del repo):

```cmd
python src\api\app.py
```

### Opción 2: Todo en uno – `full.py`

Esta opción verifica que exista `src/data/envios.json` y, si falta, intenta ejecutarlo con Java automáticamente. Requiere tener el `.jar` de Camel disponible como `src/file-transfer/file-transfer.jar`.

1) Inicia el API que se encarga de todo (desde la raíz del repo):

```cmd
python src\api\full.py
```

Si `java` no está en el PATH o no tienes Java 17, `full.py` fallará al intentar ejecutar el `.jar`.

## Endpoints principales

- GET `/envios` — Lista todos los envíos (contenido de `src/data/envios.json`).
- GET `/envios/{id_envio}` — Obtiene un envío por su ID.
- POST `/envios` — Crea un envío nuevo.

### Esquema de entrada para POST `/envios`

Body JSON (todos los campos requeridos):

```json
{
	"id_envio": "string",
	"cliente": "string",
	"direccion": "string",
	"estado": "string"
}
```

Respuestas relevantes:

- 201: creado
- 409: conflicto si `id_envio` ya existe
- 404: no encontrado (para GET por id)

## Documentación de la API

- OpenAPI local: `openapi.yaml` en la raíz del repo.
- Swagger UI: cuando el servidor esté corriendo, abre http://localhost:5000/docs
- APIFlask expone (por defecto) documentación interactiva en `/docs` y el esquema en `/openapi.json` cuando el servidor está corriendo.

## Colección Postman

Usa `IntegracionExamen1Envios.postman_collection.json` para probar los endpoints localmente.

## Stack tecnológico

- Python 3.14.0
- APIFlask 2.4.0 (microframework + OpenAPI)
- Waitress 3.0.2 (servidor WSGI de producción)
- Java 17
- Apache Camel 3.18.x (CSV → JSON)
- Maven (con `maven-shade-plugin` para generar `.jar` ejecutable)

## Notas y solución de problemas

- Si `python src\api\app.py` finaliza con error indicando que falta el archivo de datos, primero genera `src/data/envios.json` ejecutando Apache Camel (ver pasos de la Opción 1 o usar `full.py`).
- Si `python src\api\full.py` falla con "Java runtime not found", instala Java 17 y asegúrate de que `java` esté en el PATH.
- Puerto en uso: cambia `PORT` (por ejemplo, `set PORT=8000`).
- Rutas relativas: `full.py` ejecuta el `.jar` con el directorio de trabajo `src/file-transfer` para que Camel lea `envios.csv` (raíz del repo) y escriba `src/data/envios.json` correctamente.
