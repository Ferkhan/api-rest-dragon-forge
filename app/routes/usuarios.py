from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
import app.firestore_db as db
from fastapi.encoders import jsonable_encoder

from app.models import UsuarioIn, UsuarioOut

usuarios_router = APIRouter()

collection_name = "usuarios"

"""Obtener todos los usuarios"""
@usuarios_router.get("/", response_model=List[UsuarioOut], status_code=200, response_description="Lista de usuarios")
def obtener_usuarios_activos():
    response = db.readAllActives(collection_name)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios activos")
    
"""Obtener un usuario por ID"""
@usuarios_router.get("/{usuario_id}", response_model=UsuarioOut, status_code=200, response_description="Usuario encontrado")
def obtener_usuario_por_id(usuario_id: str):
    response = db.readById(collection_name, usuario_id)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
"""Crear un nuevo usuario"""
@usuarios_router.post("/", status_code=201, response_description="Usuario creado")
def crear_usuario(usuario: UsuarioIn):
    response = db.create(collection_name, usuario.model_dump())
    if response:
        return JSONResponse(content={"mensaje": "Usuario creado correctamente", "id": response}, status_code=201)
    else:
        raise HTTPException(status_code=400, detail="Error al crear el usuario")

"""Actualizar un usuario existente"""
@usuarios_router.put("/{usuario_id}", status_code=204, response_description="Usuario actualizado")
def actualizar_usuario(usuario_id: str, usuario: UsuarioIn):
    response = db.update(collection_name, usuario_id, usuario.model_dump())
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
"""Eliminar un usuario (marcar como inactivo)"""
@usuarios_router.put("/{usuario_id}/eliminar", status_code=204, response_description="Usuario marcado como eliminado")
def eliminar_usuario(usuario_id: str):
    response = db.update(collection_name, usuario_id, {"estado_registro": False})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
"""Recuperar un usuario (marcar como activo)"""
@usuarios_router.put("/{usuario_id}/recuperar", status_code=204, response_description="Usuario recuperado")
def recuperar_usuario(usuario_id: str):
    response = db.update(collection_name, usuario_id, {"estado_registro": True})
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
"""Eliminar un ejercicio (borrado físico)"""
@usuarios_router.delete("/{usuario_id}", status_code=204, response_description="Usuario borrado permanentemente")
def eliminar_usuario(usuario_id: str):
    response = db.delete(collection_name, usuario_id)
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
