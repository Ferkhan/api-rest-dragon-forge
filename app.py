from fastapi import FastAPI
from routes import rutas_ejercicios, rutas_rutinas, rutas_usuarios

def create_app() -> FastAPI:
    
    app = FastAPI(
        title="Dragon Forge API",
        description="API RESTful para gestionar ejercicios y rutinas de gimnasio",
        version="1.0.0",
    )
    
    rutas_ejercicios(app)
    rutas_rutinas(app)
    rutas_usuarios(app)

    return app