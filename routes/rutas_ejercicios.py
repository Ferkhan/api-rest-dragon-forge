import firestore_db as db
from models import EjercicioIn, EjercicioOut, EjercicioEnRutina

def rutas_ejercicios(app):
    
    # @app.get("/usuarios/{usuario_id}")
    # def obtener_usuario(usuario_id: str):
    #     doc = db.collection("usuarios").document(usuario_id).get()
    #     if doc.exists:
    #         return doc.to_dict()
    #     raise HTTPException(status_code=404, detail="Usuario no encontrado")
    collection_name = "ejercicios"

    @app.get("/ejercicios", tags=["Ejercicios"])
    def obtener_ejercicios():
        response = db.readAll(collection_name)
        return response
    
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
    def crear_ejercicio(ejercicio: EjercicioIn):
        response = db.create(collection_name, ejercicio.model_dump())
        if response:
            return {"mensaje": "Ejercicio creado correctamente", "id": response}
        else:
            return {"mensaje": "Error al crear el ejercicio"}
    
    @app.put("/ejercicios/{ejercicio_id}", tags=["Ejercicios"])
    def actualizar_ejercicio(ejercicio_id: str, ejercicio: EjercicioIn):
        response = db.update(collection_name, ejercicio_id, ejercicio.model_dump())
        if response:
            return {"mensaje": "Ejercicio actualizado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al actualizar el ejercicio"}

    @app.put("/ejercicios/{ejercicio_id}/eliminar", tags=["Ejercicios"])
    def eliminar_ejercicio(ejercicio_id: str):
        response = db.update(collection_name, ejercicio_id, {"estado_registro": False})
        if response:
            return {"mensaje": "Ejercicio eliminado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al eliminar el ejercicio"}    
        
    @app.put("/ejercicios/{ejercicio_id}/recuperar", tags=["Ejercicios"])
    def recuperar_ejercicio(ejercicio_id: str):
        response = db.update(collection_name, ejercicio_id, {"estado_registro": True})
        if response:
            return {"mensaje": "Ejercicio eliminado correctamente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al eliminar el ejercicio"}    
        
    @app.delete("/ejercicios/{ejercicio_id}", tags=["Ejercicios"])
    def borrar_ejercicio(ejercicio_id: str):
        response = db.delete(collection_name, ejercicio_id)
        if response:
            return {"mensaje": "Ejercicio borrado permanentemente", "id": ejercicio_id}
        else:
            return {"mensaje": "Error al borrar el ejercicio"}