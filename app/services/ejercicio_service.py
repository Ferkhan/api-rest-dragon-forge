
from typing import List
from fastapi import Query
from google.cloud.firestore_v1.base_query import FieldFilter
import app.firestore_db as db

collection_name = "ejercicios"

def obtener_ejercicios_activos(
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

    response = db.read_by_filters(collection_name, filters)
    
    return response
