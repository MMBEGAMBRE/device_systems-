from fastapi import FastAPI, Request
from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description="API REST profesional para la gestión de usuarios. Incluye CRUD completo, validaciones Pydantic v2 e Inyección de Dependencias.",
    version="2.0.0",
    contact={
        "name": "Maileth Begambre",
        "email": "tu-email@ejemplo.com"
    }
)

# Middleware para cabeceras
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return response

app.include_router(user_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a device_systems API v2.0"}
