from typing import List
from fastapi import Response, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import app.firestore_db as db
from app.models import EjercicioIn, EjercicioOut

ejercicios_router = APIRouter()

collection_name = "ejercicios"

"""Obtener todos los ejercicios"""
@ejercicios_router.get("/", response_model=List[EjercicioOut], status_code=200, response_description="Lista de ejercicios")
def obtener_ejercicios_activos():
    response = db.readAllActives(collection_name)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    elif not response:
        return Response(status_code=404)

"""Obtener un ejercicio por ID"""
@ejercicios_router.get("/{ejercicio_id}", response_model=EjercicioOut, status_code=200, response_description="Ejercicio encontrado")
def obtener_ejercicio_por_id(ejercicio_id: str):
    response = db.readByID(collection_name, ejercicio_id)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        return Response(status_code=404)

"""Crear un nuevo ejercicio"""
@ejercicios_router.post("/", status_code=201, response_description="Ejercicio creado")
def crear_ejercicio(ejercicio: EjercicioIn):
    response = db.create(collection_name, ejercicio.model_dump())
    if response:
        return JSONResponse(content={"mensaje": "Ejercicio creado correctamente", "id": response}, status_code=201)
    else:
        return JSONResponse(content={"mensaje": "Error al crear el ejercicio"}, status_code=400)

"""Actualizar un ejercicio existente"""
@ejercicios_router.put("/{ejercicio_id}", status_code=204, response_description="Ejercicio actualizado")
def actualizar_ejercicio(ejercicio_id: str, ejercicio: EjercicioIn):
    response = db.update(collection_name, ejercicio_id, ejercicio.model_dump())
    if response:
        return Response(status_code=204)
    else:
        return Response(status_code=404)

"""Eliminar un ejercicio (marcar como inactiva)"""
@ejercicios_router.put("/{ejercicio_id}/eliminar", status_code=204, response_description="Ejercicio marcado como eliminado")
def eliminar_ejercicio(ejercicio_id: str):
    response = db.update(collection_name, ejercicio_id, {"estado_registro": False})
    if response:
        return Response(status_code=204)
    else:
        return Response(status_code=404)
    
"""Recuperar un ejercicio (marcar como activa)"""
@ejercicios_router.put("/{ejercicio_id}/recuperar", status_code=204, response_description="Ejercicio recuperado")
def recuperar_ejercicio(ejercicio_id: str):
    response = db.update(collection_name, ejercicio_id, {"estado_registro": True})
    if response:
        return Response(status_code=204)
    else:
        return Response(status_code=404)
    
"""Eliminar un ejercicio (borrado físico)"""
@ejercicios_router.delete("/{ejercicio_id}", status_code=204, response_description="Ejercicio borrado permanentemente")
def borrar_ejercicio(ejercicio_id: str):
    response = db.delete(collection_name, ejercicio_id)
    if response:
        return Response(status_code=204)
    else:
        return Response(status_code=404)
