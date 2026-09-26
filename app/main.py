from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import app.models
from app.auth import auth_routes
from app.auth.security import limiter
from app.middlewares.request_middleware import RequestContextMiddleware
from app.routes import device_routes, loan_routes, user_routes


app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestionar usuarios, dispositivos y préstamos con SQLAlchemy, Alembic, JWT y rate limiting.",
    version="4.0.0",
    contact={
        "name": "Maileth Begambre",
        "email": "tu-email@ejemplo.com"
    },
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS: en producción no se debe combinar allow_origins=["*"] con allow_credentials=True,
# porque el navegador rechaza esa combinación y expondria las cookies/tokens a cualquier dominio.
# Por eso se listan explícitamente los orígenes del frontend autorizado.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestContextMiddleware)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a device_systems API v4.0"}
