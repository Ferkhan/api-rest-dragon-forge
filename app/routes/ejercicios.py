from typing import List
from fastapi import Query, Response, APIRouter, HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import app.firestore_db as db
from app.models import EjercicioIn, EjercicioOut, EjercicioPatch

ejercicios_router = APIRouter()

collection_name = "ejercicios"

"""Obtener todos los ejercicios"""
@ejercicios_router.get("/", response_model=List[EjercicioOut], status_code=200, response_description="Lista de ejercicios")
def obtener_ejercicios_activos():
    response = db.readAllActives(collection_name)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="No se encontraron ejercicios activos")

"""Obtener un ejercicio por ID"""
@ejercicios_router.get("/{ejercicio_id}", response_model=EjercicioOut, status_code=200, response_description="Ejercicio encontrado")
def obtener_ejercicio_por_id(ejercicio_id: str):
    response = db.readByID(collection_name, ejercicio_id)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

"""Filtrar ejercicios por grupo muscular, equipamiento y/o dificultad"""
@ejercicios_router.get("/filtrar/", response_model=List[EjercicioOut], status_code=200, response_description="Ejercicios filtrados")
def filtrar_ejercicios(
    dificultad: str = Query(default=None, description="Dificultad a filtrar"),
    equipamiento: List[str] = Query(default=None, description="Equipamiento(s) a filtrar"),
    grupo_muscular: List[str] = Query(default=None, description="Grupo(s) muscular(es) a filtrar")
):
    filters = [FieldFilter("estado_registro", "==", True)]
    if grupo_muscular:
        filters.append(FieldFilter("grupo_muscular", "array_contains", grupo_muscular))
    if equipamiento:
        filters.append(FieldFilter("equipamiento", "array_contains", equipamiento))
    if dificultad:
        filters.append(FieldFilter("dificultad", "==", dificultad))

    resultados = db.read_by_filters(collection_name, filters)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron ejercicios con los filtros dados")
    return JSONResponse(content=jsonable_encoder(resultados), status_code=200)

"""Crear un nuevo ejercicio"""
@ejercicios_router.post("/", status_code=201, response_description="Ejercicio creado")
def crear_ejercicio(ejercicio: EjercicioIn):
    response = db.create(collection_name, ejercicio.model_dump())
    if response:
        return JSONResponse(content={"mensaje": "Ejercicio creado correctamente", "id": response}, status_code=201)
    else:
        raise HTTPException(status_code=400, detail="Error al crear el ejercicio")

"""Actualizar un ejercicio existente"""
@ejercicios_router.put("/{ejercicio_id}", status_code=204, response_description="Ejercicio actualizado")
def actualizar_ejercicio(ejercicio_id: str, ejercicio: EjercicioIn):
    response = db.update(collection_name, ejercicio_id, ejercicio.model_dump())
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

"""Actualizar parcialmente un ejercicio existente"""
@ejercicios_router.patch("/{ejercicio_id}", status_code=204, response_description="Ejercicio actualizado parcialmente")
def patch_ejercicio(ejercicio_id: str, datos: EjercicioPatch):
    response = db.update(collection_name, ejercicio_id, datos.model_dump(exclude_unset=True))
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

"""Eliminar un ejercicio (marcar como inactiva)"""
@ejercicios_router.put("/{ejercicio_id}/eliminar", status_code=204, response_description="Ejercicio marcado como eliminado")
def eliminar_ejercicio(ejercicio_id: str):
    response = db.update(collection_name, ejercicio_id, {"estado_registro": False})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
"""Recuperar un ejercicio (marcar como activa)"""
@ejercicios_router.put("/{ejercicio_id}/recuperar", status_code=204, response_description="Ejercicio recuperado")
def recuperar_ejercicio(ejercicio_id: str):
    response = db.update(collection_name, ejercicio_id, {"estado_registro": True})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
"""Eliminar un ejercicio (borrado físico)"""
@ejercicios_router.delete("/{ejercicio_id}", status_code=204, response_description="Ejercicio borrado permanentemente")
def borrar_ejercicio(ejercicio_id: str):
    response = db.delete(collection_name, ejercicio_id)
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
