# Proyecto device_systems - API REST de Usuarios

Este proyecto es una API REST funcional construida con **FastAPI** para administrar los usuarios del sistema `device_systems`. Implementa validaciones con Pydantic v2, manejo de errores HTTP y documentación automática.

##  Tecnologías utilizadas
- **Python 3.14**
- **FastAPI**
- **Uvicorn** (Servidor ASGI)
- **Pydantic v2** (Validación de datos)

## Instalación y Ejecución
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el servidor: `python -m uvicorn app.main:app --reload`

##  Endpoints de la API
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/users` | Listar todos los usuarios (admite filtros por rol y estado) |
| GET | `/users/{id}` | Consultar un usuario por su ID único |
| POST | `/users` | Registrar un nuevo usuario |

##  Evidencias de Pruebas

### 1. Documentación Swagger UI
![Swagger UI](img/imagen1.jpeg)

### 2. Prueba de Listado (GET /users)
![GET Users](img/imagen2.jpeg)

### 3. Registro de Usuario (POST /users)
![POST User](img/imagen3.jpeg)

### 4. Consulta por ID
![GET by ID](img/imagen4.jpeg)

### 5. Validación de Correo Duplicado (Error 400)
![Error 400](img/imagen5.jpeg)

### 6. Validación de Datos - Pydantic (Error 422)
![Error 422](img/imagen%206.jpeg)

##  Reflexión
FastAPI permite un desarrollo ágil y profesional gracias a su tipado fuerte y validación automática. La generación instantánea de documentación (Swagger) facilita enormemente las pruebas y la colaboración en equipo.
