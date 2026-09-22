from fastapi import FastAPI, Request
from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="1.0.0"
)

# Middleware para cabeceras personalizadas
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response

# Incluir rutas
app.include_router(user_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a device_systems API"}
