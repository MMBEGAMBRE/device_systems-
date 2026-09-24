# device_systems

API REST para la gestion de usuarios, construida con FastAPI y Pydantic v2. Esta rama corresponde a la evolucion de la Guia 7 para cumplir la Guia 8.

## Tecnologias

- Python 3.10 o superior
- FastAPI
- Uvicorn
- Pydantic v2

## Estructura

```text
app/
├── data/          # Base de datos simulada en memoria
├── dependencies/  # Dependencias reutilizables con Depends()
├── routes/        # Endpoints HTTP
├── schemas/       # Modelos Pydantic de entrada y salida
└── services/      # Logica de negocio
```

## Instalacion y ejecucion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

La documentacion interactiva esta disponible en `http://127.0.0.1:8000/docs` y ReDoc en `http://127.0.0.1:8000/redoc`.

## Endpoints

| Metodo | Ruta | Descripcion | Exito | Errores principales |
| --- | --- | --- | --- | --- |
| GET | `/users` | Lista usuarios; acepta `role` e `is_active` | 200 | 422 |
| GET | `/users/{user_id}` | Consulta un usuario | 200 | 404 |
| POST | `/users` | Crea un usuario | 201 | 400, 422 |
| PUT | `/users/{user_id}` | Reemplaza todos los datos editables | 200 | 400, 404, 422 |
| PATCH | `/users/{user_id}` | Actualiza solo los campos enviados | 200 | 400, 404, 422 |
| DELETE | `/users/{user_id}` | Elimina un usuario | 204 | 404 |

Todas las respuestas incluyen `X-App-Name: device_systems` y `X-API-Version: 2.0`.

## Ejemplos

Crear un usuario:

```json
{
  "name": "Support User",
  "email": "support@example.com",
  "role": "support",
  "is_active": true
}
```

Actualizar parcialmente:

```json
{
  "role": "admin"
}
```

Un `PATCH` sin campos devuelve `400`; un ID inexistente devuelve `404`; un correo duplicado devuelve `400`; y los datos que no cumplen Pydantic devuelven `422`.

## Dependency Injection y errores

La dependencia `get_user_or_404`, ubicada en `app/dependencies/user_dependencies.py`, busca el usuario antes de ejecutar GET, PUT, PATCH o DELETE. Si no lo encuentra, lanza `HTTPException` con `404`, evitando repetir esa validacion en cada ruta. Las reglas de negocio, como correos duplicados y modificaciones, estan centralizadas en `app/services/user_service.py`.

## Evidencias de la Guia 8

Las capturas se generan desde Swagger UI y se guardan en `img/`:

- [Swagger/OpenAPI](img/guia8_swagger.png)
- [ReDoc](img/guia8_redoc.png)
- [GET /users](img/guia8_get.png)
- [POST /users](img/guia8_post.png)
- [PUT exitoso](img/guia8_put.png)
- [PATCH exitoso](img/guia8_patch.png)
- [DELETE 204](img/guia8_delete.png)
- [Error 404](img/guia8_404.png)
- [Error PATCH vacio 400](img/guia8_400.png)
- [Error de validacion 422](img/guia8_422.png)
- [Error de correo duplicado 400](img/guia8_duplicate.png)

Las evidencias de la Guia 7 se conservaron en `img/` y continuaran disponibles al publicar esta rama:

- [Evidencia 1](img/imagen1.jpeg)
- [Evidencia 2](img/imagen2.jpeg)
- [Evidencia 3](img/imagen3.jpeg)
- [Evidencia 4](img/imagen4.jpeg)
- [Evidencia 5](img/imagen5.jpeg)
- [Evidencia 6](img/imagen%206.jpeg)
