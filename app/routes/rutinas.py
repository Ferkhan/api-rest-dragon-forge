from typing import List
from fastapi import HTTPException, Response, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import app.firestore_db as db
from app.models import RutinaIn, RutinaOut

rutinas_router = APIRouter()

collection_name = "rutinas"

"""Obtener todos las rutinas"""
@rutinas_router.get("/", response_model=List[RutinaOut], status_code=200, response_description="Lista de rutinas")
def obtener_rutinas_activas():
    response = db.readAllActives(collection_name)
    if response: 
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="No se encontraron rutinas activas")
    
"""Obtener una rutina por ID"""
@rutinas_router.get("/{rutina_id}", response_model=RutinaOut, status_code=200, response_description="Rutina encontrada")
def obtener_rutina_por_id(rutina_id: str):
    response = db.readByID(collection_name, rutina_id)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

"""Crear una nueva rutina"""
@rutinas_router.post("/", status_code=201, response_description="Rutina creada")
def crear_rutina(rutina: RutinaIn):
    response = db.create(collection_name, rutina.model_dump())
    if response:
        return JSONResponse(content={"mensaje": "Rutina creada correctamente", "id": response}, status_code=201)
    else:
        raise HTTPException(status_code=400, detail="Error al crear la rutina")
    
"""Actualizar una rutina existente"""
@rutinas_router.put("/{rutina_id}", status_code=204, response_description="Rutina actualizada")
def actualizar_rutina(rutina_id: str, rutina: RutinaIn):
    response = db.update(collection_name, rutina_id, rutina.model_dump())
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    
"""Eliminar una rutina (marcar como inactiva)"""
@rutinas_router.put("/{rutina_id}/eliminar", status_code=204, response_description="Rutina marcada como eliminada")
def eliminar_rutina(rutina_id: str):
    response = db.update(collection_name, rutina_id, {"estado_registro": False})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    
"""Recuperar una rutina (marcar como activa)"""
@rutinas_router.put("/{rutina_id}/recuperar", status_code=204, response_description="Rutina recuperada")
def recuperar_rutina(rutina_id: str):
    response = db.update(collection_name, rutina_id, {"estado_registro": True})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

"""Eliminar una rutina (borrado físico)"""
@rutinas_router.delete("/{rutina_id}", status_code=204, response_description="Rutina eliminada")
def eliminar_rutina(rutina_id: str):
    response = db.delete(collection_name, rutina_id)
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")