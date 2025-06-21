from datetime import datetime
from typing import List
from google.cloud.firestore_v1.base_query import FieldFilter
from app.init_firebase import init_firebase

try:
    db = init_firebase()
    print("Firebase inicializado correctamente")
except Exception as e:
    print(f"Error al inicializar Firebase: {e}")

"""Convierte un documento de Firestore a un diccionario con su ID."""
def doc_to_dict(doc):
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None

"""Crear un nuevo documento en la colección especificada"""
def create(collection_name, data, id = None):
    try:
        data['fecha_creacion'] = datetime.now()
        data['fecha_actualizacion'] = datetime.now()

        if id:
            doc_ref = db.collection(collection_name).document(id)
        else:
            doc_ref = db.collection(collection_name).document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        print(f"Error al crear el documento: {e}")
        return None

"""Leer un documento de la colección especificada"""
def readByID(collection_name, document_id):
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc_to_dict(doc)        
        if data and data.get('estado_registro') is True:
            return data
        else:
            return None
    else:
        return None

"""Leer todos los documentos de la colección especificada"""
def readAllActives(collection_name):
    try:
        doc_ref = db.collection(collection_name)
        query = doc_ref.where(filter=FieldFilter('estado_registro', '==', True))
        docs = query.stream()
        return [doc_to_dict(doc) for doc in docs]
    except Exception as e:
        print(f"Error reading documents: {e}")
        return None
        
"""Actualizar un documento en la colección especificada"""
def update(collection_name, document_id, data):
    try:
        data['fecha_actualizacion'] = datetime.now()

        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.update(data)
        return doc_ref.id    
    except Exception as e:
        print(f"Error al actualizar el documento: {e}")
        return None

"""Eliminar un documento de la colección especificada"""
def delete(collection_name, document_id):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.delete()
        return document_id
    except Exception as e:
        print(f"Error al eliminar el documento: {e}")
        return None

"""Leer documentos de la colección especificada con filtros"""
def read_by_filters(collection_name: str, filters: List[FieldFilter]):
    doc_ref = db.collection(collection_name)
    query = doc_ref
    for f in filters:
        query = query.where(filter=f)
    docs = query.stream()
    return [doc_to_dict(doc) for doc in docs]

# def readByFilters():
#     try:
#         doc_ref = db.collection("peliculas")
        
#         query = doc_ref.where(filter=FieldFilter("anio", "==", 2008)).where(filter=FieldFilter("genero", "==", "Accion"))

#         docs = query.stream()

#         for doc in docs:
#             print(f"{doc.id} => {doc.to_dict()}")
#     except Exception as e:
#         print(f"Error al leer los documentos: {e}")
#         return None

# def readDiferentFilters():
#     # Leer documentos de la colección "peliculas" con diferentes filtros
#     doc_ref = db.collection("peliculas")
    
#     filter1 = FieldFilter("anio", "==", 2008)
#     filter2 = FieldFilter("anio", "==", 2013)
    
#     or_filter = Or(filters=[filter1, filter2])
    
#     docs = doc_ref.where(filter=or_filter).stream()

#     for doc in docs:
#         print(f"{doc.id} => {doc.to_dict()}")