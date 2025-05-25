from fastapi import FastAPI
# from routes import rutas_ejercicios, rutas_rutinas, rutas_usuarios
from app.routes import ejercicios_router
from app.routes import rutas_rutinas    
from app.routes import rutas_usuarios

def create_app() -> FastAPI:
    
    app = FastAPI(
        title="Dragon Forge API",
        description="API RESTful para gestionar ejercicios y rutinas de gimnasio",
        version="1.0.0",
    )

    @app.get("/", tags=["Inicio"])
    def inicio():
        return {"message": "Bienvenido a la API de Dragon Forge"}
    
    app.include_router(router=ejercicios_router, prefix="/ejercicios", tags=["Ejercicios"])
    rutas_rutinas(app)
    rutas_usuarios(app)

    return app