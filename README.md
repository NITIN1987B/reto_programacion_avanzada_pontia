# Task Management API

API REST para la gestión de tareas desarrollada con FastAPI.

## Instalación

### 1. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Puedes usar cualquiera de estos comandos:

```bash
# Opción 1: Comando moderno de FastAPI (recomendado)
fastapi dev main.py

# Opción 2: Uvicorn tradicional
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Endpoints

### TODO: Documentar todos los endpoints

- `GET /` - Información de la API - comprueba que la API está funcionando.
- `POST /tasks/` - Crear una nueva tarea : Hay que mandar título, contenido y deadline. 
                    Si el deadline es una fecha pasada o el título/contenido  está vacío, devuelve error 422. 
                    Si todo va bien, devuelve 201 con la tarea creada (con su id y fecha de creación)
- `GET /tasks/{task_id}` - Obtener una tarea por ID. Si no existe, da 404.
- `PUT /tasks/{task_id}/completar` - Marcar una tarea como completada. Da 404 si el id no existe, 
                                    y 400 si la tarea ya estaba completada de antes (no se puede completar dos veces).
- `GET /tasks/caducadas` - Obtener lista de tareas caducadas

## Ejecutar tests

```bash
python test_api.py
```

## Documentación interactiva

Una vez ejecutando la aplicación, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
