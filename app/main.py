from fastapi import FastAPI, Request

import app.models
from app.routes import device_routes, loan_routes, user_routes


app = FastAPI(
    title="device_systems API",
    description="API REST para gestionar usuarios, dispositivos y préstamos con SQLAlchemy, Alembic y consultas relacionales.",
    version="3.0.0",
    contact={
        "name": "Maileth Begambre",
        "email": "tu-email@ejemplo.com"
    },
)

# Middleware para cabeceras
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return response

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a device_systems API v3.0"}
