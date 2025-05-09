import app.firestore_db as db
from app.models import Ejercicio, EjercicioEnRutina

def rutas_ejercicios(app):
    collection_name = "ejercicios"

    """Obtener todos los ejercicios"""
    @app.get("/ejercicios", tags=["Ejercicios"])
    def obtener_ejercicios():
        response = db.readAll(collection_name)
        return response
    
    """Obtener un ejercicio por ID"""
    @app.get("/ejercicios/{ejercicio_id}", tags=["Ejercicios"])
    def obtener_ejercicio_por_id(ejercicio_id: str):
        response = db.readByID(collection_name, ejercicio_id)
        if response:
            return response
        else:
            return {"mensaje": "Ejercicio no encontrado"}
            # raise HTTPException(status_code=404, detail="Usuario no encontrado")

    """Crear un nuevo ejercicio"""
    @app.post("/ejercicios", tags=["Ejercicios"])
    def crear_ejercicio(ejercicio: Ejercicio):
        response = db.create(collection_name, ejercicio.model_dump())
        if response:
            return {"mensaje": "Ejercicio creado correctamente", "id": response}
        else:
            return {"mensaje": "Error al crear el ejercicio"}
    
    """Actualizar un ejercicio existente"""
    @app.put("/ejercicios/{ejercicio_id}", tags=["Ejercicios"])
    def actualizar_ejercicio(ejercicio_id: str, ejercicio: Ejercicio):
        response = db.update(collection_name, ejercicio_id, ejercicio.model_dump())
        if response:
            return {"mensaje": "Ejercicio actualizado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al actualizar el ejercicio"}

    """Eliminar un ejercicio (marcar como inactiva)"""
    @app.put("/ejercicios/{ejercicio_id}/eliminar", tags=["Ejercicios"])
    def eliminar_ejercicio(ejercicio_id: str):
        response = db.update(collection_name, ejercicio_id, {"estado_registro": False})
        if response:
            return {"mensaje": "Ejercicio eliminado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al eliminar el ejercicio"}    
        
    """Recuperar un ejercicio (marcar como activa)"""
    @app.put("/ejercicios/{ejercicio_id}/recuperar", tags=["Ejercicios"])
    def recuperar_ejercicio(ejercicio_id: str):
        response = db.update(collection_name, ejercicio_id, {"estado_registro": True})
        if response:
            return {"mensaje": "Ejercicio eliminado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al eliminar el ejercicio"}    
        
    """Eliminar un ejercicio (borrado físico)"""
    @app.delete("/ejercicios/{ejercicio_id}", tags=["Ejercicios"])
    def borrar_ejercicio(ejercicio_id: str):
        response = db.delete(collection_name, ejercicio_id)
        if response:
            return {"mensaje": "Ejercicio borrado permanentemente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al borrar el ejercicio"}