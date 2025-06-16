from fastapi import FastAPI
from app.routes import ejercicios_router
from app.routes import rutinas_router
from app.routes import usuarios_router
from fastapi.middleware.cors import CORSMiddleware # Permitir el acceso desde otros dominios

def create_app() -> FastAPI:
    
    app = FastAPI(
        title="Dragon Forge API",
        description="API RESTful para gestionar ejercicios y rutinas de gimnasio",
        version="0.3.1",
    )

    # Activar el middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],            # <-- or ["*"] si quieres permitir todos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["Inicio"])
    def inicio():
        return {"message": "Bienvenido a la API de Dragon Forge"}
    
    app.include_router(router=ejercicios_router,    prefix="/ejercicios",   tags=["Ejercicios"])
    app.include_router(router=rutinas_router,       prefix="/rutinas",      tags=["Rutinas"])
    app.include_router(router=usuarios_router,      prefix="/usuarios",     tags=["Usuarios"])

    return app