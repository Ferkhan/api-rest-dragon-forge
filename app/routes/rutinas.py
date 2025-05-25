import app.firestore_db as db
from app.models import Rutina

def rutas_rutinas(app):
    collection_name = "rutinas"

    """Obtener todas las rutinas"""
    @app.get("/rutinas", tags=["Rutinas"])
    def obtener_rutinas():
        response = db.readAllActives(collection_name)
        return response
    
    """Obtener una rutina por ID"""
    @app.get("/rutinas/{rutina_id}", tags=["Rutinas"])
    def obtener_rutina_por_id(rutina_id: str):
        response = db.readByID(collection_name, rutina_id)
        if response:
            return response
        else:
            return {"mensaje": "Rutina no encontrada"}
        
    """Crear una nueva rutina"""
    @app.post("/rutinas", tags=["Rutinas"])
    def crear_rutina(rutina: Rutina):
        response = db.create(collection_name, rutina.model_dump())
        if response:
            return {"mensaje": "Rutina creada correctamente", "id": response}
        else:
            return {"mensaje": "Error al crear la rutina"}
        
    """Actualizar una rutina existente"""
    @app.put("/rutinas/{rutina_id}", tags=["Rutinas"])
    def actualizar_rutina(rutina_id: str, rutina: Rutina):
        response = db.update(collection_name, rutina_id, rutina.model_dump())
        if response:
            return {"mensaje": "Rutina actualizada correctamente", "id": rutina_id}
        else:
            return {"mensaje": "Error al actualizar la rutina"}
        
    """Eliminar una rutina (marcar como inactiva)"""
    @app.put("/rutinas/{rutina_id}/eliminar", tags=["Rutinas"])
    def eliminar_rutina(rutina_id: str):
        response = db.update(collection_name, rutina_id, {"estado_registro": False})
        if response:
            return {"mensaje": "Rutina eliminada correctamente", "id": rutina_id}
        else:
            return {"mensaje": "Error al eliminar la rutina"}
        
    """Recuperar una rutina (marcar como activa)"""
    @app.put("/rutinas/{rutina_id}/recuperar", tags=["Rutinas"])
    def recuperar_rutina(rutina_id: str):
        response = db.update(collection_name, rutina_id, {"estado_registro": True})
        if response:
            return {"mensaje": "Rutina recuperada correctamente", "id": rutina_id}
        else:
            return {"mensaje": "Error al recuperar la rutina"}
        
    """Eliminar una rutina (borrado físico)"""
    @app.delete("/rutinas/{rutina_id}", tags=["Rutinas"])
    def eliminar_rutina(rutina_id: str):
        response = db.delete(collection_name, rutina_id)
        if response:
            return {"mensaje": "Rutina eliminada correctamente", "id": rutina_id}
        else:
            return {"mensaje": "Error al eliminar la rutina"}