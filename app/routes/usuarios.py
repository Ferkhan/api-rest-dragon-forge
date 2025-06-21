from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from firebase_admin import auth
import httpx

import app.firestore_db as db
import app.firestore_auth as fs_auth
from app.models import UsuarioIn, UsuarioLogin, UsuarioOut, UsuarioPatch, UsuarioPatchDatosFenotipicos, UsuarioRegistro

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
    response = db.readByID(collection_name, usuario_id)
    if response:
        return JSONResponse(content=jsonable_encoder(response), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
"""Registrar un nuevo usuario"""
@usuarios_router.post("/", status_code=201, response_description="Usuario creado")
def registrar_usuario(usuario: UsuarioRegistro):
    try:
        uid_user = fs_auth.create_user(usuario.email, usuario.contrasenia, usuario.nombre)
        response = db.create(collection_name, usuario.model_dump(), uid_user)        
        if not response:
            raise HTTPException(status_code=500, detail="Error al crear el usuario")            
        return JSONResponse(content={"mensaje": "Usuario creado correctamente", "id": response}, status_code=201)    
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

""""Inicio de sesión de usuario"""
@usuarios_router.post("/login", response_model=UsuarioOut, status_code=200, response_description="Inicio de sesión exitoso")
def login_usuario(usuario: UsuarioLogin):
    FIREBASE_API_KEY = "AIzaSyBmRiSbA4YAzS8GRqCsXIUypGdaHiisVsI"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    
    payload = {
        "email": usuario.email,
        "password": usuario.contrasenia,
        "returnSecureToken": True
    }

    response = httpx.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user_email = response.json()["email"]
    user = fs_auth.get_user_by_email(user_email)
    
    user_data = db.readByID(collection_name, user.uid)
    if not user_data or not user_data.get('estado_registro', True):
        raise HTTPException(status_code=404, detail="Usuario no encontrado o se encuentra inactivo")
    return JSONResponse(content=jsonable_encoder(UsuarioOut(**user_data)), status_code=200)


"""Actualizar un usuario existente"""
@usuarios_router.put("/{usuario_id}", status_code=204, response_description="Usuario actualizado")
def actualizar_usuario(usuario_id: str, usuario: UsuarioIn):
    response = db.update(collection_name, usuario_id, usuario.model_dump())
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

"""Actualizar parcialmente un usuario existente"""
@usuarios_router.patch("/{usuario_id}", status_code=204, response_description="Usuario actualizado parcialmente")
def actualizar_ejercicio_parcialmente(usuario_id: str, datos: UsuarioPatch):
    response = db.update(collection_name, usuario_id, datos.model_dump(exclude_unset=True))
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
      
"""Actualizar los datos fenotípicos de un usuario"""
@usuarios_router.patch("/{usuario_id}/fenotipo", status_code=204, response_description="Datos fenotípicos actualizados")
def actualizar_datos_fenotipicos(usuario_id: str, datos: UsuarioPatchDatosFenotipicos):
    usuario = db.readByID(collection_name, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Actualiza los campos requeridos
    update_data = datos.model_dump()
    update_data["info_fenotipica_completa"] = True
    update_data["fecha_actualizacion"] = datetime.now()
    response = db.update(collection_name, usuario_id, update_data)
    if response:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar los datos fenotípicos")

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
    try:
        fs_auth.delete_user(usuario_id)        
        response = db.delete(collection_name, usuario_id)

        if response:
            return Response(status_code=204)
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")    
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en Firebase")