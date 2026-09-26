# Proyecto device_systems - API REST de Usuarios

Este proyecto es una API REST funcional construida con **FastAPI** para administrar los usuarios del sistema `device_systems`. Implementa validaciones con Pydantic v2, manejo de errores HTTP y documentación automática.

## Tecnologías utilizadas

- **Python 3.14**
- **FastAPI**
- **Uvicorn** (Servidor ASGI)
- **Pydantic v2** (Validación de datos)

## Instalación y Ejecución

1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el servidor: `python -m uvicorn app.main:app --reload`

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/users` | Listar todos los usuarios (admite filtros por rol y estado) |
| GET | `/users/{id}` | Consultar un usuario por su ID único |
| POST | `/users` | Registrar un nuevo usuario |

## Evidencias de la Guía 7

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

## Reflexión

FastAPI permite un desarrollo ágil y profesional gracias a su tipado fuerte y validación automática. La generación instantánea de documentación (Swagger) facilita enormemente las pruebas y la colaboración en equipo.

---

# Evolución Guía 8 - CRUD Completo

La Guía 8 evoluciona esta API sin eliminar la documentación ni las evidencias de la Guía 7. Se agregaron actualización completa, actualización parcial, eliminación, manejo de errores, Dependency Injection y documentación OpenAPI ampliada.

## Nueva estructura

```text
app/
├── data/          # Base de datos simulada en memoria
├── dependencies/  # Dependencias reutilizables con Depends()
├── routes/        # Endpoints HTTP
├── schemas/       # Modelos Pydantic de entrada y salida
└── services/      # Lógica de negocio
```

## Endpoints agregados en la Guía 8

| Método | Ruta | Descripción | Éxito | Errores principales |
| --- | --- | --- | --- | --- |
| GET | `/users` | Lista usuarios; acepta `role` e `is_active` | 200 | 422 |
| GET | `/users/{user_id}` | Consulta un usuario | 200 | 404 |
| POST | `/users` | Crea un usuario | 201 | 400, 422 |
| PUT | `/users/{user_id}` | Reemplaza todos los datos editables | 200 | 400, 404, 422 |
| PATCH | `/users/{user_id}` | Actualiza solo los campos enviados | 200 | 400, 404, 422 |
| DELETE | `/users/{user_id}` | Elimina un usuario | 204 | 404 |

Todas las respuestas incluyen `X-App-Name: device_systems` y `X-API-Version: 2.0`.

## Ejemplos de actualización

PUT completo:

```json
{
  "name": "Support User",
  "email": "support@example.com",
  "role": "support",
  "is_active": true
}
```

PATCH parcial:

```json
{
  "role": "admin"
}
```

Un `PATCH` sin campos devuelve `400`; un ID inexistente devuelve `404`; un correo duplicado devuelve `400`; y los datos que no cumplen Pydantic devuelven `422`.

## Dependency Injection y errores

La dependencia `get_user_or_404`, ubicada en `app/dependencies/user_dependencies.py`, busca el usuario antes de ejecutar GET, PUT, PATCH o DELETE. Si no lo encuentra, lanza `HTTPException` con `404`, evitando repetir esa validación en cada ruta. Las reglas de negocio están centralizadas en `app/services/user_service.py`.

La documentación interactiva está disponible en `http://127.0.0.1:8000/docs` y ReDoc en `http://127.0.0.1:8000/redoc`.

## Evidencias de la Guía 8

### 1. Documentación Swagger/OpenAPI
![Swagger Guía 8](img/guia8_swagger.png)

### 2. Documentación ReDoc
![ReDoc Guía 8](img/guia8_redoc.png)

### 3. Prueba de listado (GET /users)
![GET Guía 8](img/guia8_get.png)

### 4. Registro de usuario (POST /users)
![POST Guía 8](img/guia8_post.png)

### 5. Actualización completa (PUT)
![PUT Guía 8](img/guia8_put.png)

### 6. Actualización parcial (PATCH)
![PATCH Guía 8](img/guia8_patch.png)

### 7. Eliminación de usuario (DELETE - 204)
![DELETE Guía 8](img/guia8_delete.png)

### 8. Usuario no encontrado (404)
![Error 404 Guía 8](img/guia8_404.png)

### 9. PATCH sin datos (400)
![Error 400 Guía 8](img/guia8_400.png)

### 10. Datos inválidos (422)
![Error 422 Guía 8](img/guia8_422.png)

### 11. Correo duplicado (400)
![Correo duplicado Guía 8](img/guia8_duplicate.png)

---

# Evolución Guía 9 - Persistencia con SQLAlchemy

La Guía 9 conserva las funcionalidades y evidencias históricas de las Guías 7 y 8. Las capturas anteriores documentan esas versiones; las evidencias nuevas de esta sección deben tomarse sobre la versión con SQLAlchemy. El cambio principal es que los usuarios dejan de guardarse en una lista temporal y pasan a persistirse en SQLite mediante SQLAlchemy.

## Estructura de la Guía 9

```text
app/
├── database/       # Engine, Base y configuración de sesiones
├── dependencies/  # Sesiones de base de datos reutilizables
├── models/        # Modelo ORM de SQLAlchemy
├── routes/        # Endpoints HTTP
├── schemas/       # Validación y respuesta con Pydantic
└── services/      # Consultas y operaciones CRUD
```

## Instalación y ejecución

Instala las dependencias declaradas en `requirements.txt` y ejecuta:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Se recomienda usar un entorno virtual local. En PowerShell puedes crearlo y activarlo así:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

La aplicación crea `device_systems.db` y la tabla `users` al iniciar. La base SQLite está en la raíz del proyecto y no se versiona en Git.

## SQLAlchemy y Pydantic

El modelo `User` en `app/models/user_model.py` representa la tabla física: define los tipos SQL, `created_at`, campos obligatorios, email único y una restricción para limitar `role` a `admin`, `support` o `user`.

Los schemas de `app/schemas/user_schema.py` no son tablas. Pydantic valida los datos que entran a la API y estructura las respuestas. `UserResponse` usa `from_attributes=True` para construir la respuesta a partir de una instancia ORM.

`get_db()` crea una sesión por petición y la cierra al terminar. Las rutas la reciben mediante `Depends()` y delegan las consultas a `app/services/user_service.py`. La lista y búsqueda permiten filtros por rol/estado y orden con `sort_by=name` o `sort_by=created_at`.

## Respuestas principales

| Situación | Código |
| --- | --- |
| Consulta correcta | 200 |
| Usuario creado | 201 |
| Actualización completa o parcial | 200 |
| Usuario eliminado | 204 |
| Usuario inexistente | 404 |
| Email duplicado | 400 |
| Datos rechazados por Pydantic | 422 |

## Evidencias de la Guía 9

Las tres primeras capturas fueron tomadas manualmente y se conservaron con sus nombres originales. Las capturas restantes muestran ejecuciones realizadas en Swagger UI y documentación servida por la API.

### Estructura del proyecto
![Estructura de la Guía 9](img/guia9_base_estructura.jpeg)

### Base de datos SQLite
![Base de datos de la Guía 9](img/guia9_base_datos.jpeg)

### Swagger UI
![Swagger UI de la Guía 9](img/guia9_swagger.jpeg)

### ReDoc
![ReDoc de la Guía 9](img/guia9_redoc.png)

### POST exitoso (201)
![POST exitoso de la Guía 9](img/guia9_post.png)

### GET de lista (200)
![Listado de usuarios de la Guía 9](img/guia9_get_list.png)

### GET con filtro por rol (200)
![Filtro de usuarios de la Guía 9](img/guia9_get_filter.png)

### GET por ID (200)
![Consulta por ID de la Guía 9](img/guia9_get_id.png)

### PUT completo (200)
![PUT de la Guía 9](img/guia9_put.png)

### PATCH parcial (200)
![PATCH de la Guía 9](img/guia9_patch.png)

### DELETE (204)
![DELETE de la Guía 9](img/guia9_delete.png)

### Consulta del usuario eliminado (404)
![Usuario eliminado no encontrado](img/guia9_deleted_404.png)

### Usuario inexistente (404)
![Error 404 de la Guía 9](img/guia9_get_404.png)

### Email duplicado (400)
![Error por email duplicado de la Guía 9](img/guia9_duplicate.png)

### Validación Pydantic (422)
![Error de validación de la Guía 9](img/guia9_validation_422.png)

## Reflexión sobre persistencia

Con SQLAlchemy los datos sobreviven al reinicio de la API porque se guardan en SQLite. Separar el modelo ORM de los schemas Pydantic permite distinguir la estructura de la base de datos de los datos que acepta y entrega la API. Las constraints de la base de datos refuerzan las validaciones y protegen la integridad incluso si una petición concurrente intenta registrar un email repetido.

---

# Evolución Guía 10 - Alembic, relaciones y consultas

La Guía 10 conserva usuarios de las actividades anteriores y agrega dispositivos y préstamos. Un `Loan` referencia un `User` y un `Device`; al prestar un dispositivo se marca no disponible y al devolverlo vuelve a estar disponible. Alembic controla los cambios de esquema.

## Estructura añadida

```text
alembic/
└── versions/
app/
├── database/       # Engine y Base
├── dependencies/  # Sesión SQLAlchemy por petición
├── models/        # User, Device y Loan relacionados
├── routes/        # Users, Devices y Loans
├── schemas/       # Validación Pydantic v2
└── services/      # CRUD, reglas de préstamos y consultas con joins
```

## Instalar, migrar y ejecutar

Activa el entorno virtual e instala `requirements.txt`:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si ya tienes la base de la Guía 9 con `users` y todavía no tiene historial Alembic, registra esa tabla existente una sola vez y aplica las migraciones nuevas:

```powershell
alembic stamp aa55df750f10
alembic upgrade head
alembic history
python -m uvicorn app.main:app --reload
```

`stamp` solo registra el baseline existente; no crea ni borra tablas o filas. En una instalación limpia, usa directamente `alembic upgrade head`: el baseline crea `users` y la siguiente revisión crea `devices` y `loans`.

Para futuras modificaciones del modelo, genera y aplica una revisión:

```powershell
alembic revision --autogenerate -m "describe el cambio"
alembic upgrade head
```

La revisión `aa55df750f10` conserva el esquema User de Guía 9 y lo crea únicamente si falta. La revisión `8e88a3c46e3c` crea las tablas de dispositivos y préstamos; está protegida para no duplicar tablas que ya existan.

## Relaciones y validaciones

- Un usuario tiene muchos préstamos (`User.loans`).
- Un dispositivo tiene muchos préstamos históricos (`Device.loans`).
- Cada préstamo referencia un usuario y un dispositivo con claves foráneas.
- Los números de serie son únicos; los tipos de equipo y estados tienen constraints y validación Pydantic.
- No se presta un equipo no disponible ni se devuelve dos veces el mismo préstamo.
- Los registros históricos impiden borrar usuarios o dispositivos relacionados.

El modelo SQLAlchemy define tablas, tipos, relaciones y constraints. Los schemas Pydantic validan los datos de entrada y determinan el formato de respuesta, incluidos los objetos anidados del detalle de préstamo.

## Endpoints de la Guía 10

| Método | Ruta | Función |
| --- | --- | --- |
| GET, POST, PUT, PATCH, DELETE | `/users` y `/users/{user_id}` | CRUD de usuarios conservado |
| GET | `/users/{user_id}/loans` | Historial del usuario con dispositivos relacionados |
| GET, POST | `/devices` | Listar/filtrar y registrar dispositivos |
| GET, PUT, PATCH, DELETE | `/devices/{device_id}` | Consultar y administrar dispositivos |
| GET | `/devices/{device_id}/loans` | Historial del dispositivo |
| GET | `/loans` | Listar y filtrar préstamos con usuario y dispositivo |
| GET | `/loans/details` | Consulta relacional detallada |
| GET | `/loans/{loan_id}` | Consultar un préstamo detallado |
| POST | `/loans` | Crear préstamo y actualizar disponibilidad |
| PATCH | `/loans/{loan_id}/return` | Registrar devolución y liberar dispositivo |

Filtros de dispositivos: `device_type`, `is_available`, `brand`, `search` y `sort_by`. Filtros de préstamos: `status`, `user_email`, `device_type`, `user_id`, `device_id`, `from_date` y `to_date`. Las consultas de préstamos usan joins entre las tres tablas.

## Códigos HTTP

| Caso | Código |
| --- | --- |
| Crear usuario, dispositivo o préstamo | 201 |
| Consultar, actualizar o devolver | 200 |
| Eliminar dispositivo sin historial | 204 |
| Usuario, dispositivo o préstamo inexistente | 404 |
| Email o serial duplicado | 400 |
| Dispositivo no disponible, préstamo ya devuelto o historial que impide borrar | 409 |
| Entrada o filtro inválido | 422 |

La documentación OpenAPI está disponible en `/docs` y `/redoc`. Las respuestas HTTP conservan `X-App-Name` y `X-API-Version: 3.0`.

## Evidencias de la Guía 10

Conserva las evidencias de las Guías 7, 8 y 9. Las siguientes corresponden a la versión con Alembic, relaciones entre `users`, `devices` y `loans`, y consultas con joins.

### Migraciones con Alembic

#### Estructura de Alembic inicializada
![Alembic inicializado](img/guia10_alembic_init.jpeg)

#### Migración generada (`alembic revision --autogenerate`)
![Migración generada](img/guia10_revision.jpeg)

#### Migración aplicada (`alembic upgrade head`)
![Migración aplicada](img/guia10_upgrade.jpeg)

### Estructura de las tablas generadas

#### Tabla `devices`
![Estructura de devices](img/guia10_tablas_devices.jpeg)

#### Tabla `loans` (con foreign keys hacia `users` y `devices`)
![Estructura de loans](img/guia10_tablas_loans.jpeg)

#### Tabla `users`
![Estructura de users](img/guia10_tablas_users.jpeg)

### Documentación de la API

#### Swagger UI con los grupos Users, Devices y Loans
![Swagger UI Guía 10](img/guia10_swagger.jpeg)

#### ReDoc
![ReDoc Guía 10](img/guia10_redoc.png)

### Pruebas funcionales

#### Registro de usuario (`POST /users`)
![POST usuario](img/guia10_user_post.png)

#### Registro de dispositivo (`POST /devices`)
![POST dispositivo](img/guia10_device_post.png)

#### Registro de préstamo (`POST /loans`) con usuario y dispositivo anidados
![POST préstamo](img/guia10_loan_post.png)

#### Intento de préstamo con dispositivo no disponible (`409`)
![Préstamo no disponible](img/guia10_loan_unavailable.png)

#### Consulta con joins (`GET /loans/details`)
![Consulta con joins](img/guia10_loan_details.png)

#### Filtros aplicados (`GET /loans?status=active`)
![Filtros de préstamos](img/guia10_loan_filters.png)

#### Historial de préstamos del usuario (`GET /users/{user_id}/loans`)
![Historial del usuario](img/guia10_user_history.png)

#### Historial de préstamos del dispositivo (`GET /devices/{device_id}/loans`)
![Historial del dispositivo](img/guia10_device_history.png)

#### Devolución de préstamo (`PATCH /loans/{loan_id}/return`)
![Devolución de préstamo](img/guia10_loan_return.png)

#### Dispositivo disponible después de la devolución
![Dispositivo disponible](img/guia10_device_available.png)

### Errores controlados

#### Correo duplicado (`400`)
![Error 400](img/guia10_error_400.jpeg)

#### Recurso no encontrado (`404`)
![Error 404](img/guia10_error_404.jpeg)

#### Préstamo ya devuelto (`409`)
![Error 409](img/guia10_error_409.jpeg)

## Reflexión sobre relaciones y migraciones

Alembic permite revisar y aplicar cambios del esquema de manera repetible sin recrear la base ni perder los datos existentes. Las relaciones y claves foráneas conectan usuarios, dispositivos y préstamos, mientras que los joins permiten responder consultas completas en una sola API. La disponibilidad coordinada con el estado del préstamo evita entregar dos veces el mismo equipo y conservar un historial verificable.